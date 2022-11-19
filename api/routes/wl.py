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

# from api.models.nm_aquifer_models import (
#     WaterLevels,
#     WaterLevelsContinuous_Pressure,
#     WaterLevelsContinuous_Acoustic,
#     Location,
# )
from api.models.wl_models import WellMeasurement, Well, Location, ObservedProperty

from api.routes import _read, get_waterdb, Params
from api.schemas import wl_schemas

router = APIRouter()


@router.get(
    "/waterlevels",
    response_model=List[wl_schemas.WellMeasurement],
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
        js.extend([Well, Location])
        fs.append(Location.point_id == point_id)
    elif location_id:
        js.extend([Well, Location])
        fs.append(Location.id == location_id)

    vs = _read(
        db,
        WellMeasurement,
        joins=js,
        filters=fs,
        orderby=WellMeasurement.timestamp,
    )
    print(vs)
    return paginate(vs, params)


@router.get(
    "/welltemperatures",
    response_model=List[wl_schemas.WellMeasurement],
    tags=["Groundwater Temperatures"],
)
def read_temperatures(
    point_id: str = None, db: Session = Depends(get_waterdb), params: Params = Depends()
):
    fs = [ObservedProperty.name == "WellTemperature"]
    js = [ObservedProperty]
    if point_id:
        js.extend([Well, Location])
        fs.append(Location.point_id == point_id)

    vs = _read(
        db,
        WellMeasurement,
        joins=js,
        filters=fs,
        orderby=WellMeasurement.timestamp,
    )

    return paginate(vs, params)


#
# @router.get(
#     "/waterlevelspressure",
#     response_model=List[nm_aquifer_schemas.WaterLevelsPressure],
#     tags=["Groundwater Levels"],
# )
# def read_waterlevelspressure(
#         pointid: str = None, limit: int = 1000, db: Session = Depends(get_nm_aquifer)
# ):
#     if pointid:
#         fs = [WaterLevelsContinuous_Pressure.PointID == pointid]
#     return _read(db, WaterLevelsContinuous_Pressure, limit, filters=fs)
#
#
# @router.get(
#     "/waterlevelsacoustic",
#     response_model=List[nm_aquifer_schemas.WaterLevelsAcoustic],
#     tags=["Groundwater Levels"],
# )
# def read_waterlevelspressure(
#         pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
# ):
#     return _read(db, WaterLevelsContinuous_Acoustic, limit)
#
#
@router.get("/locations", response_model=Page[wl_schemas.Location], tags=["Locations"])
def read_locations(
    point_id: str = None,
    public_release: bool = None,
    db: Session = Depends(get_waterdb),
    params: Params = Depends(),
):
    filters = []
    if point_id:
        filters.append(Location.point_id == point_id)

    if public_release is not None:
        filters.append(Location.public_release == public_release)

    return paginate(_read(db, Location, filters=filters), params)


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
        joins.append(Location)
        filters.append(Location.point_id == point_id)
    elif location_id:
        filters.append(Well.location_id == location_id)

    return paginate(_read(db, Well, joins=joins, filters=filters), params)


# ============= EOF =============================================
