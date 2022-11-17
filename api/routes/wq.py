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
from api.models.nm_water_quality_models import WQ_Arsenic, WQ_Bicarbonate, WQ_Calcium, WQ_Chlorine, WQ_Fluoride, \
    WQ_Magnesium, WQ_Sodium, WQ_Sulfate, WQ_TDS, WQ_Uranium

from api.routes import _read, get_nm_aquifer
from api.schemas import nm_aquifer_schemas, nm_water_quality_schemas
from fastapi import APIRouter, Depends

from api.session import NM_Aquifer, NM_Water_Quality
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/majorchemistry", response_model=List[nm_aquifer_schemas.MajorChemistry], tags=['Water Quality'])
def read_majorchemistry(pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)):
    filters = []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MajorChemistry, limit=limit, filters=filters)


@router.get("/minorchemistry", response_model=List[nm_aquifer_schemas.MinorandTraceChemistry], tags=['Water Quality'])
def read_minorchemistry(pointid: str = None, limit: int = 100, db: Session = Depends(get_nm_aquifer)):
    filters = []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MinorandTraceChemistry, limit=limit, filters=filters)


@router.get('/compiled/arsenic', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_arsenic(limit: int = 100, pointid: str = None, datasource: str = None,
                          db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Arsenic, limit, pointid, datasource)


@router.get('/compiled/bicarbonate', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_bicarbonate(limit: int = 100, pointid: str = None, datasource: str = None,
                              db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Bicarbonate, limit, pointid, datasource)


@router.get('/compiled/calcium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_calcium(limit: int = 100, pointid: str = None, datasource: str = None,
                          db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Calcium, limit, pointid, datasource)


@router.get('/compiled/chlorine', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_chlorine(limit: int = 100, pointid: str = None, datasource: str = None,
                           db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Chlorine, limit, pointid, datasource)


@router.get('/compiled/fluoride', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_fluoride(limit: int = 100, pointid: str = None, datasource: str = None,
                           db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Fluoride, limit, pointid, datasource)


@router.get('/compiled/magnesium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_magnesium(limit: int = 100, pointid: str = None, datasource: str = None,
                            db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Magnesium, limit, pointid, datasource)


@router.get('/compiled/sodium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_sodium(limit: int = 100, pointid: str = None, datasource: str = None,
                         db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Sodium, limit, pointid, datasource)


@router.get('/compiled/sulfate', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_sulfate(limit: int = 100, pointid: str = None, datasource: str = None,
                          db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Sulfate, limit, pointid, datasource)


@router.get('/compiled/tds', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_tds(limit: int = 100, pointid: str = None, datasource: str = None,
                      db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_TDS, limit, pointid, datasource)


@router.get('/compiled/uranium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_uranium(limit: int = 100, pointid: str = None, datasource: str = None,
                          db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Uranium, limit, pointid, datasource)


def _read_compiled_chem(db, table, limit, pointid, datasource):
    filters = []
    if pointid:
        filters.append(table.POINT_ID == pointid)
    if datasource:
        filters.append(table.DataSource == datasource)

    return _read(db, table, limit, filters=filters)
# ============= EOF =============================================
