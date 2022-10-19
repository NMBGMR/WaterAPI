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
from datetime import datetime, date, time
from typing import List, Optional

from pydantic import BaseModel, Field



class ORMBase(BaseModel):

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class Location(ORMBase):
    LocationId: uuid.UUID
    DateCreated: datetime
    PointID: str
    SiteNames: Optional[str]=None
    # SiteID
    # AlternateSiteID
    # AlternateSiteID2
    SiteDate: Optional[datetime]=None
    #DataReliability: str
    Confidential: bool
    # SiteType: str
    WL_Continuous: bool
    WL_Intermittent: bool
    WaterQuality: bool
    WaterFlow: bool
    Hydraulic: bool
    Subsurface: bool
    WellorSpgNoData: bool
    SubsurfaceType: Optional[str]
    Easting: int
    Northing: int
    UTMDatum: str
    CoordinateNotes: str
    Altitude: float
    AltitudeAccuracy: Optional[float]
    # AltitudeMethod: Optional[str]
    AltDatum: Optional[str]
    # Latitude: Optional[float]
    # Longitude: Optional[float]
    # LatLonDatum: str
    CoordinateAccuracy: Optional[str]
    CoordinateMethod: Optional[str]
    Township: Optional[int]
    TownshipDirection: Optional[str]
    Range: Optional[int]
    RangeDirection: Optional[str]
    SectionQuarters: Optional[float]
    # SPX
    # SPY
    QuadName: Optional[str]
    County: Optional[str]
    State: str
    LocationNotes: Optional[str]
    WLReportDeliver: Optional[datetime]
    ChemistryReportDeliver: Optional[datetime]
    WLReportNote: Optional[str]
    ChemistryReportNote: Optional[str]
    X_NAD83_Zone12: float
    Y_NAD83_Zone12: float
    projectname: Optional[str]
    USGSProjectID: Optional[str]
    # ObjectID
    LatitudeDD: float
    LongitudeDD: float
    # SSMA_TimeStamp
    PublicRelease: bool
    # Geometry

    altitude_method_meaning: str = Field(..., alias='AltitudeMethodMeaning')
    coordinate_accuracy_meaning: Optional[str] = Field(..., alias='CoordinateAccuracyMeaning')
    data_reliability_meaning: Optional[str] = Field(..., alias='DataReliabilityMeaning')
    site_type_meaning:Optional[str] = Field(..., alias='SiteTypeMeaning')

class Chemistry(ORMBase):
    SamplePtID: uuid.UUID
    SamplePointID: str
    Analyte: str
    Symbol: Optional[str]
    SampleValue: float
    Units: str
    Uncertainty: Optional[float]
    AnalysisMethod: Optional[str]
    AnalysisDate: Optional[datetime]
    Notes: Optional[str]
    Volume: Optional[int]
    VolumeUnit: Optional[str]
    # OBJECTID
    # GlobalID
    AnalysesAgency: Optional[str]
    WCLab_ID: Optional[str]

class MajorChemistry(Chemistry):
    pass

class MinorandTraceChemistry(Chemistry):
    pass

class WaterLevelsBase(ORMBase):
    WellID: uuid.UUID
    PointID: str
    OBJECTID: int
    DepthToWaterBGS: float
    measurement_method_meaning: str=Field(alias='MeasurementMethodMeaning')

class WaterLevels(WaterLevelsBase):

    DepthToWater: float
    LevelStatus: Optional[str]
    # DataQuality: Optional[str]
    MPHeight: float
    # MeasurementMethod: str
    MeasuredBy: Optional[str]
    # DataSource: str
    MeasuringAgency: Optional[str]
    SiteNotes: Optional[str]
    LevelStatement: Optional[str]
    PublicRelease: bool
    DateMeasured: date
    TimeMeasured: Optional[time]
    TimeDatum: Optional[str]

    data_quality_meaning: Optional[str]=Field(alias='DataQualityMeaning')
    data_source_meaning: Optional[str]=Field(alias='DataSourceMeaning')


class WaterLevelsPressure(WaterLevelsBase):
    DateMeasured: datetime
    TemperatureWater: float
    # WaterHead
    # WaterHeadAdjusted
    DepthToWaterBGS: float
    # MeasurementMethod
    # DataSource
    # MeasuringAgency
    QCed: bool
    Notes: str
    Created: Optional[datetime]
    Updated: Optional[datetime]
    ProcessedBy: Optional[str]
    CheckedBy: Optional[str]
    conddl: Optional[str]

class WaterLevelsAcoustic(WaterLevelsBase):
    TemperatureAir: str
    Notes: Optional[str]
    SerialNo: Optional[str]
    ServerReceiptDate: Optional[datetime]
    WellntelReadingType: Optional[str]
    SensorHgtAboveMP: Optional[float]
    SpeakerToMicLength: Optional[int]
    PublicRelease: bool
    Created: Optional[datetime]
    EventID: Optional[str]
    ImportID: Optional[str]
# ============= EOF =============================================
