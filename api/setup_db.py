# ===============================================================================
# Copyright 2022 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os

import pymssql
import pyproj as pyproj
from geoalchemy2 import Geometry
from api.config import settings
from api.models.wl_models import (
    Base,
    Location,
    Well,
    ObservedProperty,
    WellMeasurement,
    WellConstruction,
    ScreenInterval,
    Project,
    ProjectLocation,
    LU_DataSource,
    LU_MeasurementMethod,
    LU_Status,
    LU_CurrentUse,
    LU_AquiferType,
    LU_AquiferClass,
)
from api.nm_aquifer_connector import (
    get_associated_projects,
    get_screens,
    get_welldata,
    get_manual_water_levels,
    get_lookup_by_name,
    get_pressure_water_levels,
    get_projects,
    get_gw_locations,
    get_acoustic_water_levels,
    LOCATION_CHUNK,
)
from api.session import waterdbengine, WATERDB, NM_Aquifer


def setup_db_default():
    if int(os.environ["DATABASE_DEV"]):
        # Base.metadata.drop_all(bind=waterdbengine)
        # Base.metadata.create_all(bind=waterdbengine)

        db = WATERDB()
        db.add(Location(point_id="JR-001", point="Point(-105 35)"))
        db.add(Location(point_id="JR-002", point="Point(-104 34)"))
        db.commit()

        w1 = Well(location_id=1)
        w2 = Well(location_id=2)
        db.add(w1)
        db.add(w2)
        db.add(WellConstruction(well=w1))
        db.add(WellConstruction(well=w2))
        db.add(ObservedProperty(name="DepthToWaterBGS"))
        db.add(ObservedProperty(name="WellTemperature"))
        db.commit()
        db.add(WellMeasurement(well_id=1, value=10, observed_property_id=1))
        db.add(WellMeasurement(well_id=2, value=131, observed_property_id=1))

        db.add(WellMeasurement(well_id=1, value=103, observed_property_id=2))
        db.commit()
        db.close()


def copy_db():
    db = WATERDB()

    copy_nm_aquifer(db)

    db.commit()
    db.close()


def copy_lu(cursor, dest, table, tag=None):
    if tag is None:
        tag = table.__tablename__

    sql = f"select * from dbo.{tag}"
    cursor.execute(sql)
    for li in cursor.fetchall():
        d = table(name=li["CODE"], meaning=li["MEANING"])
        dest.add(d)
    dest.commit()
    dest.flush()


def copy_gw_location(projection, cursor, dest, obsprop_bgs, l):
    lon, lat = projection(l["Easting"], l["Northing"], inverse=True)
    # print(f'adding location {l["PointID"]}')
    dbloc = Location(
        point_id=l["PointID"],
        elevation=l["Altitude"],
        elevation_datum=l["AltDatum"],
        point=f"POINT({lon} {lat})",
        township=l["Township"],
        township_direction=l["TownshipDirection"],
        range=l["Range"],
        range_direction=l["RangeDirection"],
        public_release=l["PublicRelease"],
        county=l["County"],
        state=l["State"],
        quad=l["QuadName"],
        notes=l["LocationNotes"],
    )
    dest.add(dbloc)

    # add location to associated projects
    for ap in get_associated_projects(cursor, l["PointID"]):
        q = dest.query(Project).filter(Project.name == ap["ProjectName"])
        dest.add(ProjectLocation(project=q.first(), location=dbloc))

    screens = get_screens(cursor, l["PointID"])
    wd = get_welldata(cursor, l["PointID"])
    wckw = {}
    wkw = {}
    if wd:
        wd = wd[0]
        wckw = dict(
            construction_method=wd["ConstructionMethod"],
            construction_notes=wd["ConstructionNotes"],
            casing_diameter=wd["CasingDiameter"],
            casing_depth=wd["CasingDepth"],
            casing_description=wd["CasingDescription"],
            well_depth=wd["WellDepth"],
            hole_depth=wd["HoleDepth"],
            measuring_point_height=wd["MPHeight"],
            measuring_point=wd["MeasuringPoint"],
        )
        wkw = dict(
            ose_well_id=wd["OSEWellID"],
            ose_well_tag_id=wd["OSEWelltagID"],
            aquifer_class_id=get_lookup_by_name(dest, LU_AquiferClass, wd["AqClass"]),
            aquifer_type_id=get_lookup_by_name(dest, LU_AquiferType, wd["AquiferType"]),
            formation=wd["FormationZone"],
            current_use_id=get_lookup_by_name(dest, LU_CurrentUse, wd["CurrentUse"]),
            status_id=get_lookup_by_name(dest, LU_Status, wd["Status"]),
        )

    dbwell = Well(location=dbloc, **wkw)
    dest.add(dbwell)
    dbscreens = [
        ScreenInterval(
            top=i["ScreenTop"],
            bottom=i["ScreenTop"],
            description=i["ScreenDescription"],
        )
        for i in screens
    ]
    dbwc = WellConstruction(well=dbwell, screens=dbscreens, **wckw)
    dest.add(dbwc)

    # copy waterlevels
    for wl in get_manual_water_levels(cursor, l["PointID"]):
        dsid = get_lookup_by_name(dest, LU_DataSource, wl["DataSource"])
        mmid = get_lookup_by_name(dest, LU_MeasurementMethod, wl["MeasurementMethod"])
        dest.add(
            WellMeasurement(
                well=dbwell,
                value=wl["DepthToWaterBGS"],
                timestamp=wl["DateTimeMeasured"],
                public_release=wl["PublicRelease"],
                data_source_id=dsid,
                method_id=mmid,
                measuring_agency=wl["MeasuringAgency"],
                measured_by=wl["MeasuredBy"],
                observed_property=obsprop_bgs,
            )
        )
    dest.commit()
    # copy continuous
    ptid = get_lookup_by_name(dest, LU_MeasurementMethod, "Pressure Transducer")
    aid = get_lookup_by_name(dest, LU_MeasurementMethod, "Acoustic")

    def pressure_payload(r):
        return dict(public_release=True)

    def acoustic_payload(r):
        return dict(public_release=r["PublicRelease"])

    for (mmid, func, payload) in (
        (ptid, get_pressure_water_levels, pressure_payload),
        (aid, get_acoustic_water_levels, acoustic_payload),
    ):
        for wl in func(cursor, l["PointID"]):
            dest.add(
                WellMeasurement(
                    well=dbwell,
                    value=wl["DepthToWaterBGS"],
                    timestamp=wl["DateMeasured"],
                    method_id=mmid,
                    observed_property=obsprop_bgs,
                    **payload(wl),
                )
            )
        dest.commit()


def copy_gw_locations(cursor, dest, obsprop_bgs, locations):
    projection = pyproj.Proj(proj="utm", zone=int(13), ellps="WGS84")
    failures = []
    locations =list(locations)
    total = len(locations)
    for i, l in enumerate(locations):
        if l["SiteType"] != "GW":
            continue
        try:
            copy_gw_location(projection, cursor, dest, obsprop_bgs, l)
        except BaseException:
            failures.append(l)

        printProgressBar(i, total, prefix=f'Sync PointID={l["PointID"]}', suffix='Complete')

    return failures


def copy_nm_aquifer(dest):
    src = pymssql.connect(*settings.NM_AQUIFER_ARGS)
    cursor = src.cursor(as_dict=True)

    # copy projects
    projects = get_projects(cursor)
    for p in projects:
        dbp = Project(name=p["Project"], point_id_prefix=p["PointIDPrefix"])
        dest.add(dbp)
    dest.commit()
    dest.flush()

    # make obsproperties
    obsprop_bgs = ObservedProperty(name="DepthToWaterBGS")
    dest.add(obsprop_bgs)
    # obsprop_wt = ObservedProperty(name="WellTemperature")
    # dest.add(obsprop_wt)

    # copy LUs
    copy_lu(cursor, dest, LU_DataSource)
    copy_lu(cursor, dest, LU_MeasurementMethod)
    copy_lu(cursor, dest, LU_Status)
    copy_lu(cursor, dest, LU_CurrentUse)
    copy_lu(cursor, dest, LU_AquiferType)
    copy_lu(cursor, dest, LU_AquiferClass)

    # copy  public locations
    pfailures = copy_gw_locations(
        cursor, dest, obsprop_bgs, get_gw_locations(cursor, public_release="true")
    )
    dest.commit()
    print(f"public location failures. {pfailures}")

    # copy non public locations
    npfailures = copy_gw_locations(
        cursor, dest, obsprop_bgs, get_gw_locations(cursor, public_release="false")
    )
    print(f"public non location failures. {npfailures}")

    dest.commit()
    src.close()


# Print iterations progress
def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# ============= EOF =============================================
