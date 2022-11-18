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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


waterdbengine = create_engine(settings.WATERDB_URL)
nm_aquifer_engine = create_engine(settings.NM_AQUIFER_URL)
# nm_water_quality_engine = create_engine(settings.NM_WATER_QUALITY_URL)

# if you don't want to install postgres or any database, use sqlite, a file system based database,
# uncomment below lines if you would like to use sqlite and comment above 2 lines of SQLALCHEMY_DATABASE_URL AND engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# print(SQLALCHEMY_DATABASE_URL)
NM_Aquifer = sessionmaker(autocommit=False, autoflush=False, bind=nm_aquifer_engine)
# NM_Water_Quality = sessionmaker(
#     autocommit=False, autoflush=False, bind=nm_water_quality_engine
# )

WATERDB = sessionmaker(autocommit=False, autoflush=False, bind=waterdbengine)
# ============= EOF =============================================
