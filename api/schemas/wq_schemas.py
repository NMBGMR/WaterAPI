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
from datetime import datetime
from typing import Optional, Any
from geoalchemy2 import Geometry
from geojson_pydantic.geometries import Point

from pydantic.main import BaseModel

from api.schemas.wl_schemas import WellMeasurement


class ORMBase(BaseModel):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ObservedProperty(ORMBase):
    name: str
    group: Optional[str]
    units: Optional[str]
    definition: Optional[str]


class MajorChemistry(WellMeasurement):
    observed_property: ObservedProperty

# ============= EOF =============================================
