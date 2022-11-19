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
)
from api.session import waterdbengine, WATERDB, NM_Aquifer


def setup_db_default():
    if int(os.environ["DATABASE_DEV"]):
        Base.metadata.drop_all(bind=waterdbengine)
        Base.metadata.create_all(bind=waterdbengine)

        db = WATERDB()
        db.add(Location(point_id="JR-001", point='Point(-105 35)'))
        db.add(Location(point_id="JR-002", point='Point(-104 34)'))
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


def setup_db():

    db = WATERDB()
    if int(os.environ["COPY_NM_AQUIFER"]):
        copy_nm_aquifer(db)

    db.commit()
    db.close()


def get_locations(cursor):
    def func():
        i = 0
        while 1:
            sql = f"""select * from dbo.Location 
--             where PointID like 'AB-%' 
            order by PointID
            offset {i*100} rows fetch next 100 rows only
            """
            cursor.execute(sql)
            records = cursor.fetchall()
            if not records:
                break
            yield from records

            i += 1

    return func()


def get_screens(cursor, pointid):
    sql = "select * from dbo.WellScreens where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_welldata(cursor, pointid):
    sql = "select * from dbo.WellData where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_projects(cursor):
    sql = "select * from dbo.Projects"
    return fetch(cursor, sql)


def get_associated_projects(cursor, pointid):
    sql = "select * from dbo.ProjectLocations where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_manual_water_levels(cursor, pointid):
    sql = """select (CASE
     WHEN TimeMeasured is NULL 
     then CONVERT(DateTime, DateMeasured) 
        else
       CONVERT(DateTime, DateMeasured) + CONVERT(DateTime, TimeMeasured) 
       end) as DateTimeMeasured, * from dbo.WaterLevels where PointID=%s order by DateMeasured"""
    return fetch(cursor, sql, pointid)


def fetch(cursor, sql, *args):
    cursor.execute(sql, *args)
    return cursor.fetchall()


def get_lookup_by_name(dest, table, name):
    q = dest.query(table).filter(table.name == name)
    try:
        return q.first().id
    except AttributeError:
        pass


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

    # copy LU_Datasource
    copy_lu(cursor, dest, LU_DataSource)
    copy_lu(cursor, dest, LU_MeasurementMethod)

    # copy locations
    # locations =
    projection = pyproj.Proj(proj="utm", zone=int(13), ellps="WGS84")
    for l in get_locations(cursor):

        lon, lat = projection(l["Easting"], l["Northing"], inverse=True)

        print(f'adding location {l["PointID"]}')
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

        if l["SiteType"] == "GW":
            dbwell = Well(location=dbloc)
            dest.add(dbwell)
            screens = get_screens(cursor, l["PointID"])
            wd = get_welldata(cursor, l["PointID"])
            wdkw = {}
            if wd:
                wd = wd[0]
                wdkw = dict(
                    casing_diameter=wd["CasingDiameter"],
                    well_depth=wd["WellDepth"],
                    hole_depth=wd["HoleDepth"],
                    measuring_point_height=wd["MPHeight"],
                )
            dbscreens = [
                ScreenInterval(
                    top=i["ScreenTop"],
                    bottom=i["ScreenTop"],
                    description=i["ScreenDescription"],
                )
                for i in screens
            ]
            dbwc = WellConstruction(well=dbwell, screens=dbscreens, **wdkw)
            dest.add(dbwc)

            # copy waterlevels
            for wl in get_manual_water_levels(cursor, l["PointID"]):
                dsid = get_lookup_by_name(dest, LU_DataSource, wl["DataSource"])
                mmid = get_lookup_by_name(
                    dest, LU_MeasurementMethod, wl["MeasurementMethod"]
                )

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
    src.close()


# ============= EOF =============================================
