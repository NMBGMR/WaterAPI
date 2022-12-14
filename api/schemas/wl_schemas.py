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


class ORMBase(BaseModel):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Location(ORMBase):
    point_id: str
    latitude: float
    longitude: float
    county: Optional[str]


class WellConstruction(ORMBase):
    measuring_point: Optional[str]
    measuring_point_height: Optional[float]
    casing_diameter: Optional[float]
    casing_depth: Optional[float]
    casing_description: Optional[str]

    hole_depth: Optional[float]
    well_depth: Optional[float]

    construction_method: Optional[str]
    construction_notes: Optional[str]


class Thing(ORMBase):
    public_release: bool
    aquifer_class: Optional[str]
    aquifer_type: Optional[str]
    formation: Optional[str]
    current_use: Optional[str]
    status: Optional[str]


class Well(ORMBase):
    ose_well_id: Optional[str]
    ose_well_tag_id: Optional[str]
    well_construction: WellConstruction
    thing: Thing


class Measurement(ORMBase):
    value: float
    timestamp: datetime
    # well: Well


# ============= EOF =============================================
