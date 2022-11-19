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
from http.client import HTTPException

from api.session import WATERDB


# from api.session import NM_Aquifer, NM_Water_Quality


# def get_nm_aquifer():
#     db = NM_Aquifer()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# def get_nm_water_quality():
#     db = NM_Water_Quality()
#     try:
#         yield db
#     finally:
#         db.close()


from typing import TypeVar, Generic

from fastapi import Query

from fastapi_pagination.default import Page as BasePage, Params as BaseParams

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(500, ge=1, le=1_000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params


def get_waterdb():
    db = WATERDB()
    try:
        yield db
    finally:
        db.close()


def _read(db, table, joins=None, limit=None, filters=None, orderby=None):
    q = db.query(table)
    if joins:
        for ji in joins:
            q = q.join(ji)

    if filters:
        for fi in filters:
            q = q.filter(fi)

    if orderby:
        q = q.order_by(orderby)
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
