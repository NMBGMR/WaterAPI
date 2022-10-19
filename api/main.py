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
from api.models import Location, MajorChemistry, MinorandTraceChemistry, WaterLevels, WaterLevelsContinuous_Pressure, \
    WaterLevelsContinuous_Acoustic
from api.session import engine, SessionLocal

tags_metadata = [
    # {"name": "wells", "description": "Water Wells"},
    # {"name": "repairs", "description": "Meter Repairs"},
    # {"name": "meters", "description": "Water use meters"},
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/locations", response_model=List[schemas.Location], tags=['Locations'])
def read_locations(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):
    filters =  []
    if pointid:
        filters = [Location.PointID==pointid]
    return _read(db, Location, limit=limit, filters=filters)


@app.get("/majorchemistry", response_model=List[schemas.MajorChemistry], tags=['Water Quality'])
def read_majorchemistry(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):
    filters =  []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MajorChemistry, limit=limit, filters=filters)

@app.get("/minorchemistry", response_model=List[schemas.MinorandTraceChemistry], tags=['Water Quality'])
def read_minorchemistry(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):
    filters =  []
    if pointid:
        pass
        # filters = [MajorChemistry.PointID==pointid]

    return _read(db, MinorandTraceChemistry, limit=limit, filters=filters)


@app.get("/waterlevels", response_model=List[schemas.WaterLevels], tags=['Groundwater Levels'])
def read_waterlevels(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):

    return _read(db, WaterLevels, limit)

@app.get("/waterlevelspressure", response_model=List[schemas.WaterLevelsPressure],tags=['Groundwater Levels'])
def read_waterlevelspressure(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):

    return _read(db, WaterLevelsContinuous_Pressure, limit)


@app.get("/waterlevelsacoustic", response_model=List[schemas.WaterLevelsAcoustic],tags=['Groundwater Levels'])
def read_waterlevelspressure(pointid:str=None, limit: int= 100, db: Session = Depends(get_db)):

    return _read(db, WaterLevelsContinuous_Acoustic, limit)

@app.get("/")
async def index():
    return {"message": "NMBGMR Water API"}


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
