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

from api.models.nm_aquifer_models import MajorChemistry, MinorandTraceChemistry
from api.models.nm_water_quality_models import (
    WQ_Arsenic,
    WQ_Bicarbonate,
    WQ_Calcium,
    WQ_Chlorine,
    WQ_Fluoride,
    WQ_Magnesium,
    WQ_Sodium,
    WQ_Sulfate,
    WQ_TDS,
    WQ_Uranium,
)
from api.models.wl_models import Location, WellMeasurement, Well, ObservedProperty
from api.schemas import wq_schemas
from api.routes import _read, get_waterdb
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/majorchemistry/{point_id}",
    response_model=List[wq_schemas.MajorChemistry],
    tags=["Water Quality"],
)
def read_chemistry(point_id: str, db: Session = Depends(get_waterdb)):
    js = [Well, Location, ObservedProperty]
    fs = [Location.point_id == point_id,
          ObservedProperty.group == "water_chemistry"]

    return _read(db, WellMeasurement, filters=fs, joins=js)

# @router.get(
#     "/majorchemistry",
#     response_model=List[nm_aquifer_schemas.MajorChemistry],
#     tags=["Water Quality"],
# )
# def read_majorchemistry(
#     point_id: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
# ):
#     filters = []
#     if point_id:
#         pass
#         # filters = [MajorChemistry.PointID==point_id]
#
#     return _read(db, MajorChemistry, limit=limit, filters=filters)
#
#
# @router.get(
#     "/minorchemistry",
#     response_model=List[nm_aquifer_schemas.MinorandTraceChemistry],
#     tags=["Water Quality"],
# )
# def read_minorchemistry(
#     point_id: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)
# ):
#     filters = []
#     if point_id:
#         pass
#         # filters = [MajorChemistry.PointID==point_id]
#
#     return _read(db, MinorandTraceChemistry, limit=limit, filters=filters)
#
#
# @router.get(
#     "/compiled/arsenic",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_arsenic(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Arsenic, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/bicarbonate",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_bicarbonate(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Bicarbonate, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/calcium",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_calcium(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Calcium, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/chlorine",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_chlorine(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Chlorine, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/fluoride",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_fluoride(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Fluoride, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/magnesium",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_magnesium(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Magnesium, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/sodium",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_sodium(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Sodium, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/sulfate",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_sulfate(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Sulfate, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/tds",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_tds(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_TDS, limit, point_id, datasource)
#
#
# @router.get(
#     "/compiled/uranium",
#     response_model=List[nm_water_quality_schemas.CompiledChem],
#     tags=["CompiledChem"],
# )
# def read_compiled_uranium(
#     limit: int = 100,
#     point_id: str = None,
#     datasource: str = None,
#     db: Session = Depends(get_nm_water_quality),
# ):
#     return _read_compiled_chem(db, WQ_Uranium, limit, point_id, datasource)
#
#
# def _read_compiled_chem(db, table, limit, point_id, datasource):
#     filters = []
#     if point_id:
#         filters.append(table.POINT_ID == point_id)
#     if datasource:
#         filters.append(table.DataSource == datasource)
#
#     return _read(db, table, limit, filters=filters)
#

# ============= EOF =============================================
