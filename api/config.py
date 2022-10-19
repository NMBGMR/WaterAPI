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

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    # DB_PORT: str = os.getenv(
    #     "DB_PORT", 5432
    # )  # default postgres port is 5432
    DB_NAME: str = os.getenv("DB_NAME", "tdd")
    DB_DRIVER: str = os.getenv("DB_DRIVER", 'mssql')
    DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


settings = Settings()
# ============= EOF =============================================
