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
from typing import List
from fastapi_pagination import add_pagination, Page, paginate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from numpy import polyfit

# from api.models.nm_aquifer_models import (
#     WaterLevels,
#     WaterLevelsContinuous_Pressure,
#     WaterLevelsContinuous_Acoustic,
#     Location,
# )
from api.models.models import (
    Measurement,
    Well,
    Location,
    ObservedProperty,
    ProjectLocation,
    Project,
    Thing,
)

from api.routes import _read, get_waterdb, Params
from api.schemas import wl_schemas

router = APIRouter()


@router.get(
    "/waterlevels",
    response_model=Page[wl_schemas.Measurement],
    tags=["Groundwater Levels"],
)
def read_waterlevels(
    point_id: str = None,
    location_id: int = None,
    db: Session = Depends(get_waterdb),
    params: Params = Depends(),
):
    fs = [ObservedProperty.name == "DepthToWaterBGS"]
    js = [ObservedProperty]
    if point_id:
        js.extend([Thing, Location])
        fs.append(Location.point_id == point_id)
    elif location_id:
        js.extend([Thing, Location])
        fs.append(Location.id == location_id)

    return paginate(
        _read(
            db,
            Measurement,
            joins=js,
            filters=fs,
            orderby=Measurement.timestamp,
        ),
        params,
    )
    # return paginate(vs, params)


@router.get(
    "/welltemperatures",
    response_model=Page[wl_schemas.Measurement],
    tags=["Groundwater Temperatures"],
)
def read_temperatures(
    point_id: str = None, db: Session = Depends(get_waterdb), params: Params = Depends()
):
    fs = [ObservedProperty.name == "WellTemperature"]
    js = [ObservedProperty]
    if point_id:
        js.extend([Thing, Location])
        fs.append(Location.point_id == point_id)

    vs = _read(
        db,
        Measurement,
        joins=js,
        filters=fs,
        orderby=Measurement.timestamp,
    )

    return paginate(vs, params)


#
# @router.get(
#     "/waterlevelspressure",
#     response_model=List[nm_aquifer_schemas.WaterLevelsPressure],
#     tags=["Groundwater Levels"],
# )
# def read_waterlevelspressure(
#         point_id: str = None, limit: int = 1000, db: Session = Depends(get_nm_aquifer)
# ):
#     if point_id:
#         fs = [WaterLevelsContinuous_Pressure.PointID == point_id]
#     return _read(db, WaterLevelsContinuous_Pressure, limit, filters=fs)
#
#
# @router.get(
#     "/waterlevelsacoustic",
#     response_model=List[nm_aquifer_schemas.WaterLevelsAcoustic],
#     tags=["Groundwater Levels"],
# )
# def read_waterlevelspressure(
#         point_id: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
# ):
#     return _read(db, WaterLevelsContinuous_Acoustic, limit)
#
#
def write_user():
    pass


def add_item(db, item):
    db.add_item(item)
    db.commit()
    db.refresh_item(item)
    return item


@router.post(
    "/locations",
    dependencies=[Depends(write_user)],
    response_model=wl_schemas.Location,
    tags=["Locations"],
)
def add_location(location: wl_schemas.Location, db: Session = Depends(get_waterdb)):
    db_item = Location(**location.dict())
    return add_item(db, db_item)


@router.post(
    "/things",
    dependencies=[Depends(write_user)],
    response_model=wl_schemas.Thing,
    tags=["Things"],
)
def add_thing(thing: wl_schemas.Thing, db: Session = Depends(get_waterdb)):
    db_item = Thing(**thing.dict())
    return add_item(db, db_item)


@router.post(
    "/wells",
    dependencies=[Depends(write_user)],
    response_model=wl_schemas.Well,
    tags=["Well"],
)
def add_well(well: wl_schemas.Well, db: Session = Depends(get_waterdb)):
    db_item = Thing(**well.dict())
    return add_item(db, db_item)


@router.get("/locations", response_model=Page[wl_schemas.Location], tags=["Locations"])
def read_locations(
    point_id: str = None,
    project: str = None,
    public_release: bool = None,
    db: Session = Depends(get_waterdb),
    params: Params = Depends(),
):
    filters = []
    joins = []
    if point_id:
        filters.append(fuzzy_search(Location.point_id, point_id))

    if project:
        joins.extend((ProjectLocation, Project))
        filters.append(fuzzy_search(Project.name, project))

    if public_release is not None:
        filters.append(Location.public_release == public_release)

    return paginate(_read(db, Location, joins=joins, filters=filters), params)


def fuzzy_search(column, searchterm):
    if "%" in searchterm or "_" in searchterm:
        return column.like(searchterm)
    else:
        return column == searchterm


@router.get("/wells", response_model=Page[wl_schemas.Well], tags=["Wells"])
def read_wells(
    location_id: int = None,
    point_id: str = None,
    db: Session = Depends(get_waterdb),
    params: Params = Depends(),
):
    joins = []
    filters = []
    if point_id:
        joins.append(Thing)
        joins.append(Location)
        filters.append(fuzzy_search(Location.point_id, point_id))
    elif location_id:
        joins.append(Thing)
        filters.append(Thing.location_id == location_id)

    return paginate(_read(db, Well, joins=joins, filters=filters), params)


def calculate_trend(obs):
    x = [i.timestamp.timestamp() for i in obs]
    y = [i.value for i in obs]
    coeffs = polyfit(x, y, 1)
    return coeffs[0]


@router.get("/gwtrend/{point_id}", tags=["Trends"])
def read_trend(point_id: str, db: Session = Depends(get_waterdb)):
    q = db.query(Measurement)
    q = q.join(ObservedProperty, Thing, Location)
    q = q.filter(Location.point_id == point_id)
    ms = (
        q.filter(ObservedProperty.name == "DepthToWaterBGS")
        .order_by(Measurement.timestamp.desc())
        .limit(10)
        .all()
    )
    trend = 0
    if ms:
        trend = calculate_trend(ms)
    return {"trend": trend}


# ============= EOF =============================================
