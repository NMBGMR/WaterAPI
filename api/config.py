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
from dotenv import load_dotenv

from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "NMBGMR Water API"
    PROJECT_VERSION: str = "0.0.1"

    def __init__(self):
        db_user = os.getenv("NM_AQUIFER_USER")
        db_password = os.getenv("NM_AQUIFER_PASSWORD")
        db_host = os.getenv("NM_AQUIFER_HOST", "localhost")
        # DB_PORT = os.getenv(
        #     "NM_AQUIFER_PORT", 5432
        # )  # default postgres port is 5432
        db_name = os.getenv("NM_AQUIFER_NAME", "NM_Aquifer")
        db_driver = os.getenv("NM_AQUIFER_DRIVER", "mssql+pymssql")
        self.NM_AQUIFER_URL = (
            f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}"
        )

        db_user = os.getenv("NM_WATER_QUALITY_USER", db_user)
        db_password = os.getenv("NM_WATER_QUALITY_PASSWORD", db_password)
        db_host = os.getenv("NM_WATER_QUALITY_HOST", db_host)

        db_name = os.getenv("NM_WATER_QUALITY_NAME", "NM_Water_Quality")
        db_driver = os.getenv("NM_WATER_QUALITY_DRIVER", db_driver)
        self.NM_WATER_QUALITY_URL = (
            f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}"
        )


settings = Settings()
# ============= EOF =============================================
