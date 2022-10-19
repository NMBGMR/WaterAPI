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
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ORMBase(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Location(ORMBase):
    LocationId: uuid.UUID
    DateCreated: datetime

    # PointID
    # SiteNames
    # SiteID
    # AlternateSiteID
    # AlternateSiteID2
    # SiteDate
    # DataReliability
    # Confidential
    # SiteType
    # WL_Continuous
    # WL_Intermittent
    # WaterQuality
    # WaterFlow
    # Hydraulic
    # Subsurface
    # WellorSpgNoData
    # SubsurfaceType
    # Easting
    # Northing
    # UTMDatum
    # CoordinateNotes
    # Altitude
    # AltitudeAccuracy
    # AltitudeMethod
    # AltDatum
    # Latitude
    # Longitude
    # LatLonDatum
    # CoordinateAccuracy
    # CoordinateMethod
    # Township
    # TownshipDirection
    # Range
    # RangeDirection
    # SectionQuarters
    # SPX
    # SPY
    # QuadName
    # County
    # State
    # LocationNotes
    # WLReportDeliver
    # ChemistryReportDeliver
    # WLReportNote
    # ChemistryReportNote
    # X_NAD83_Zone12
    # Y_NAD83_Zone12
    # projectname
    # USGSProjectID
    # ObjectID
    # LatitudeDD
    # LongitudeDD
    # SSMA_TimeStamp
    # PublicRelease
    # Geometry
# ============= EOF =============================================
