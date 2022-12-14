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
import datetime
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.models.nm_aquifer_models import Base as aqbase
from api.models.nm_water_quality_models import Base as wqbase

# from api.routes import get_nm_aquifer, get_nm_water_quality
from api.routes import get_waterdb

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

aqbase.metadata.create_all(bind=engine)
wqbase.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# app.dependency_overrides[get_nm_aquifer] = override_get_db
# app.dependency_overrides[get_nm_water_quality] = override_get_db
app.dependency_overrides[get_waterdb] = override_get_db
client = TestClient(app)


def test_read_water_levels():
    resp = client.get("/waterlevels")
    assert resp.status_code == 200


def test_read_welltemperatures():
    resp = client.get("/welltemperatures")
    assert resp.status_code == 200


# def test_read_water_levels_pressure():
#     resp = client.get("/waterlevelspressure")
#     assert resp.status_code == 200
#
#
# def test_read_water_levels_acoustic():
#     resp = client.get("/waterlevelsacoustic")
#     assert resp.status_code == 200
#
#
# def test_read_locations():
#     resp = client.get("/locations")
#     assert resp.status_code == 200
#
#
# def test_compiled_chem():
#     for p in (
#         "arsenic",
#         "bicarbonate",
#         "calcium",
#         "chlorine",
#         "fluoride",
#         "magnesium",
#         "sodium",
#         "sulfate",
#         "tds",
#         "uranium",
#     ):
#         resp = client.get(f"/compiled/{p}")
#         assert resp.status_code == 200
#

# def test_read_repair_report():
#     response = client.get("/repair_report")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 4
#     assert data[0]["meter_serial_number"] == "1992-4-1234"
#     assert data[0]["e_read"] == "E 2412341"
#     assert data[0]["h2o_read"] == 638.831
#
#
# def test_read_meters():
#     response = client.get("/meters")
#     assert response.status_code == 200
#     data = response.json()
#     assert data[0]["serial_number"] == "1992-4-1234"
#     assert data[0]["name"] == "moo"
#     assert data[1]["name"] == "tor"
#     assert data[2]["name"] == "hag"
#
#
# def test_patch_alert():
#     response = client.patch("/alerts/1", json={"alert": "patched alert"})
#     assert response.status_code == 200
#
#
# def test_read_alerts():
#     response = client.get("/alerts")
#     assert response.status_code == 200
#     assert response.json()[0]["alert"] == "patched alert"
#     assert response.json()[0]["meter_serial_number"] == "1992-4-1234"
#     assert "open_timestamp" in response.json()[0].keys()
#     assert response.json()[0]["closed_timestamp"] is None
#     assert response.json()[0]["active"]
#
#
# def test_patch_alert_closed():
#     response = client.patch(
#         "/alerts/1", json={"closed_timestamp": datetime.datetime.now().isoformat()}
#     )
#     assert response.status_code == 200
#
#
# def test_read_wells():
#     response = client.get("/wells")
#     assert response.status_code == 200
#     assert sorted(response.json()[0].keys()) == [
#         "id",
#         "latitude",
#         "location",
#         "longitude",
#         "name",
#         "osepod",
#         "owner_id",
#     ]
#
#
# #
# #
# def test_post_meter():
#     response = client.post(
#         "/meters",
#         json={
#             "id": 10,
#             "name": "foo",
#             "serial_id": 1234,
#             "serial_case_diameter": 4,
#             "serial_year": 1992,
#         },
#     )
#     assert response.status_code == 200
#     response = client.get("/meters")
#     assert response.status_code == 200
#     assert len(response.json()) == 4
#
#
# def test_post_alert():
#     response = client.post("/alerts", json={"meter_id": 1, "alert": "this is an alert"})
#     assert response.status_code == 200
#     response = client.get("/alerts")
#     assert response.status_code == 200
#     assert len(response.json()) == 2
#
#
# def test_read_alert():
#     response = client.get("/alerts/1")
#     assert response.status_code == 200
#
#
# def test_api_status():
#     response = client.get("/api_status")
#     assert response.status_code == 200
#     assert response.json() == {"ok": True}
#
#
# def test_meter_status_lu():
#     response = client.get("/meter_status_lu")
#     assert response.status_code == 200
#
#     data = response.json()
#     assert len(data) == 3
#     assert data[0]["name"] == "POK"
#     assert data[0]["description"] == "Pump OK"


# spatial queries not compatible with spatialite
# def test_read_wells_spatial():
#     response = client.get('/wells?radius=50&latlng=35.4,-105.2')
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 1
# ============= EOF =============================================
