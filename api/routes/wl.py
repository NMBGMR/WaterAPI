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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models.nm_aquifer_models import (
    WaterLevels,
    WaterLevelsContinuous_Pressure,
    WaterLevelsContinuous_Acoustic,
    Location,
)
from api.routes import _read, get_nm_aquifer
from api.schemas import nm_aquifer_schemas

router = APIRouter()


@router.get(
    "/waterlevels",
    response_model=List[nm_aquifer_schemas.WaterLevels],
    tags=["Groundwater Levels"],
)
def read_waterlevels(
    pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
):
    return _read(db, WaterLevels, limit)


@router.get(
    "/waterlevelspressure",
    response_model=List[nm_aquifer_schemas.WaterLevelsPressure],
    tags=["Groundwater Levels"],
)
def read_waterlevelspressure(
    pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
):
    return _read(db, WaterLevelsContinuous_Pressure, limit)


@router.get(
    "/waterlevelsacoustic",
    response_model=List[nm_aquifer_schemas.WaterLevelsAcoustic],
    tags=["Groundwater Levels"],
)
def read_waterlevelspressure(
    pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
):
    return _read(db, WaterLevelsContinuous_Acoustic, limit)


@router.get(
    "/locations", response_model=List[nm_aquifer_schemas.Location], tags=["Locations"]
)
def read_locations(
    pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
):
    filters = []
    if pointid:
        filters = [Location.PointID == pointid]
    return _read(db, Location, limit=limit, filters=filters)


# ============= EOF =============================================
