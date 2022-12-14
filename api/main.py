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
# import os
# import sys
# from threading import Thread
#
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(BASE_DIR)
# # sys.path.append(BASE_DIR)
#
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_pagination import add_pagination
#
# from api.models.models import Base
# from api.session import waterdbengine
#
# # # from api.routes.wq import router as wq_router
# from api.routes.wl import router as wl_router
# from api.routes.wq import router as wq_router
# from api.routes.report import router as report_router
# from api.setup_db import setup_db_default, copy_db, copy_water_chemistry
#
# tags_metadata = [
#     {"name": "Locations", "description": ""},
#     {"name": "Groundwater Levels", "description": ""},
#     {"name": "Water Quality", "description": ""},
#     {"name": "CompiledChem", "description": ""},
# ]
# description = """
# NMBGMR Water API
# """
# title = "NMBGMR Water API"
#
# app = FastAPI(
#     title=title,
#     description=description,
#     openapi_tags=tags_metadata,
#     version="0.2.0",
# )
#
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:8000",
#     "https://localhost",
#     "http://flask2.nmbgmr.nmt.edu",
#     "http://host.docker.internal",
#     "http://amp.nmbgmr.nmt.edu",
#     "https://localhost:8000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(wl_router)
# app.include_router(wq_router)
# app.include_router(report_router)
# add_pagination(app)
#
# # app.include_router(wq_router)
#
# setup_db_default()


# @app.get("/")
# async def index():
#     return {"message": "NMBGMR Water API"}
#
#
# def get_user():
#     if not os.environ.get("GET_USER_DEV") == "1":
#         raise HTTPException(403)
#
#
# @app.get("/copy_nm_aquifer", dependencies=[Depends(get_user)])
# async def copy_nm_aquifer():
#     # t = Thread(target=copy_db)
#     # t.start()
#     return True
#
#
# @app.get("/copy_nm_aquifer_chemistry", dependencies=[Depends(get_user)])
# async def copy_nm_aquifer_chemistry():
#     # t = Thread(target=copy_water_chemistry)
#     # t.start()
#     return True


# ============= EOF =============================================
