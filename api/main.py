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
from datetime import datetime, timedelta, date

from fastapi import FastAPI, Depends, HTTPException

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from api import schemas
from api.models.nm_aquifer_models import Location, MajorChemistry, MinorandTraceChemistry, WaterLevels, WaterLevelsContinuous_Pressure, \
    WaterLevelsContinuous_Acoustic
from api.models.nm_water_quality_models import WQ_Arsenic, WQ_Bicarbonate, WQ_Calcium, WQ_Chlorine, WQ_Fluoride, \
    WQ_Magnesium, WQ_Sodium, WQ_Sulfate, WQ_TDS, WQ_Uranium
from api.session import NM_Aquifer, NM_Water_Quality
from api.schemas import nm_aquifer_schemas, nm_water_quality_schemas

tags_metadata = [
    {"name": "Locations", "description": ""},
    {"name": "Groundwater Levels", "description": ""},
    {"name": "Water Quality", "description": ""},
    {"name": "CompiledChem", "description": ""},
]
description = """
NMBGMR Water API
"""
title = "NMBGMR Water API"

app = FastAPI(
    title=title,
    description=description,
    openapi_tags=tags_metadata,
    version="0.2.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://localhost",
    "https://localhost:3000",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_nm_aquifer():
    db = NM_Aquifer()
    try:
        yield db
    finally:
        db.close()

def get_nm_water_quality():
    db = NM_Water_Quality()
    try:
        yield db
    finally:
        db.close()

@app.get("/locations", response_model=List[nm_aquifer_schemas.Location], tags=['Locations'])
def read_locations(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):
    filters =  []
    if pointid:
        filters = [Location.PointID==pointid]
    return _read(db, Location, limit=limit, filters=filters)


@app.get("/majorchemistry", response_model=List[nm_aquifer_schemas.MajorChemistry], tags=['Water Quality'])
def read_majorchemistry(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):
    filters =  []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MajorChemistry, limit=limit, filters=filters)

@app.get("/minorchemistry", response_model=List[nm_aquifer_schemas.MinorandTraceChemistry], tags=['Water Quality'])
def read_minorchemistry(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):
    filters =  []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MinorandTraceChemistry, limit=limit, filters=filters)


@app.get("/waterlevels", response_model=List[nm_aquifer_schemas.WaterLevels], tags=['Groundwater Levels'])
def read_waterlevels(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):

    return _read(db, WaterLevels, limit)

@app.get("/waterlevelspressure", response_model=List[nm_aquifer_schemas.WaterLevelsPressure],tags=['Groundwater Levels'])
def read_waterlevelspressure(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):

    return _read(db, WaterLevelsContinuous_Pressure, limit)


@app.get("/waterlevelsacoustic", response_model=List[nm_aquifer_schemas.WaterLevelsAcoustic],tags=['Groundwater Levels'])
def read_waterlevelspressure(pointid:str=None, limit: int= 100, db: Session = Depends(get_nm_aquifer)):

    return _read(db, WaterLevelsContinuous_Acoustic, limit)


@app.get('/compiled/arsenic', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_arsenic(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Arsenic, limit, pointid, datasource)

@app.get('/compiled/bicarbonate', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_bicarbonate(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Bicarbonate, limit, pointid, datasource)

@app.get('/compiled/calcium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_calcium(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Calcium, limit, pointid, datasource)

@app.get('/compiled/chlorine', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_chlorine(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Chlorine, limit, pointid, datasource)

@app.get('/compiled/fluoride', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_fluoride(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Fluoride, limit, pointid, datasource)

@app.get('/compiled/magnesium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_magnesium(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Magnesium, limit, pointid, datasource)

@app.get('/compiled/sodium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_sodium(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Sodium, limit, pointid, datasource)

@app.get('/compiled/sulfate', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_sulfate(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Sulfate, limit, pointid, datasource)

@app.get('/compiled/tds', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_tds(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_TDS, limit, pointid, datasource)


@app.get('/compiled/uranium', response_model=List[nm_water_quality_schemas.CompiledChem], tags=['CompiledChem'])
def read_compiled_uranium(limit: int=100, pointid:str=None, datasource:str=None, db: Session = Depends(get_nm_water_quality)):
    return _read_compiled_chem(db, WQ_Uranium, limit, pointid, datasource)


@app.get("/")
async def index():
    return {"message": "NMBGMR Water API"}


def _read_compiled_chem(db, table, limit, pointid, datasource):
    filters = []
    if pointid:
        filters.append(table.POINT_ID == pointid)
    if datasource:
        filters.append(table.DataSource==datasource)

    return _read(db, table, limit, filters=filters)

def _read(db, table, limit=None, filters=None):
    q = db.query(table)
    if filters:
        for fi in filters:
            q = q.filter(fi)

    if limit:
        q = q.limit(limit)

    return q.all()


def _patch(db, table, dbid, obj):
    db_item = _get(db, table, dbid)
    for k, v in obj.dict(exclude_unset=True).items():
        try:
            setattr(db_item, k, v)
        except AttributeError:
            continue

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def _add(db, table, obj):
    db_item = table(**obj.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def _delete(db, table, dbid):
    db_item = _get(db, table, dbid)
    db.delete(db_item)
    db.commit()
    return {"ok": True}


def _get(db, table, dbid):
    db_item = db.get(table, dbid)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"{table}.{dbid} not found")

    return db_item

# ============= EOF =============================================
