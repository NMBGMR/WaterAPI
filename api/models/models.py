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
from typing import Any

# from sqlalchemy_utils import UUIDType
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKeyConstraint,
    ForeignKey,
    Float,
    BLOB,
    DateTime,
    LargeBinary,
    func,
    Boolean,
    Date,
    Time,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base:
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class Project(Base):
    name = Column(String)
    point_id_prefix = Column(String)
    note = Column(String)


class ProjectLocation(Base):
    project_id = Column(Integer, ForeignKey("Project.id"))
    location_id = Column(Integer, ForeignKey("Location.id"))

    project = relationship("Project", cascade="all, delete")
    location = relationship("Location", cascade="all, delete")


class EquivalentLocation(Base):
    location_id = Column(Integer, ForeignKey("Location.id"))
    equivalent_id = Column(String)
    agency = Column(String)


class Tag(Base):
    name = Column(String)
    description = Column(String)


class LocationTag(Base):
    location_id = Column(Integer, ForeignKey("Location.id"))
    tag_id = Column(Integer, ForeignKey("Tag.id"))


class Location(Base):
    point = Column(Geometry("POINT", 4326))
    point_id = Column(String)
    elevation = Column(Float)
    elevation_datum = Column(String)
    public_release = Column(Boolean, default=False)
    state = Column(String, default="NM")
    county = Column(String)
    quad = Column(String)
    notes = Column(String)

    township = Column(Integer)
    township_direction = Column(String)
    range = Column(Integer)
    range_direction = Column(String)
    section = Column(Integer)
    quarter = Column(Integer)
    half_quarter = Column(Integer)
    quarter_quarter = Column(Integer)

    @property
    def latitude(self):
        return to_shape(self.point).y

    @property
    def longitude(self):
        return to_shape(self.point).x


class Thing(Base):
    location_id = Column(Integer, ForeignKey("Location.id"))
    location = relationship("Location")
    public_release = Column(Boolean, default=False)

    formation_id = Column(Integer, ForeignKey("LU_Formation.id"))
    aquifer_class_id = Column(Integer, ForeignKey("LU_AquiferClass.id"))
    aquifer_type_id = Column(Integer, ForeignKey("LU_AquiferType.id"))
    status_id = Column(Integer, ForeignKey("LU_Status.id"))
    current_use_id = Column(Integer, ForeignKey("LU_CurrentUse.id"))

    files = relationship("ThingFile", back_populates="thing")

    aquifer_class_ = relationship("LU_AquiferClass")
    aquifer_type_ = relationship("LU_AquiferType")
    current_use = relationship("LU_CurrentUse")
    status_ = relationship("LU_Status")

    @property
    def aquifer_class(self):
        return self.aquifer_class_.meaning

    @property
    def aquifer_type(self):
        return self.aquifer_type_.meaning

    @property
    def current_use(self):
        return self.current_use_.meaning

    @property
    def status(self):
        return self.status_.meaning


class Well(Base):
    well_construction = relationship(
        "WellConstruction", back_populates="well", uselist=False
    )
    thing_id = Column(Integer, ForeignKey("Thing.id"))
    thing = relationship("Thing", uselist=False)
    ose_well_id = Column(String)
    ose_well_tag_id = Column(String)


class Surface(Base):
    thing_id = Column(Integer, ForeignKey("Thing.id"))


class WellConstruction(Base):
    measuring_point = Column(String)
    measuring_point_height = Column(Float)
    casing_diameter = Column(Float, default=0)
    casing_depth = Column(Float)
    casing_description = Column(String)

    hole_depth = Column(Float, default=0)
    well_depth = Column(Float, default=0)

    construction_method = Column(String)
    construction_notes = Column(String)

    well_id = Column(Integer, ForeignKey("Well.id"))
    well = relationship("Well", back_populates="well_construction", uselist=False)
    screens = relationship("ScreenInterval")


class ThingFile(Base):
    path = Column(String)
    thing_id = Column(Integer, ForeignKey("Thing.id"))
    thing = relationship("Thing", back_populates="files")


class ScreenInterval(Base):
    top = Column(Float)
    bottom = Column(Float)
    description = Column(String)
    well_construction_id = Column(Integer, ForeignKey("WellConstruction.id"))


class ObservedProperty(Base):
    name = Column(String)
    units = Column(String)
    definition = Column(String)
    group = Column(String)


class Measurement(Base):
    value = Column(Float)
    error = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    thing_id = Column(Integer, ForeignKey("Thing.id"))
    method_id = Column(Integer, ForeignKey("LU_MeasurementMethod.id"))
    observed_property_id = Column(Integer, ForeignKey("ObservedProperty.id"))
    sensor_id = Column(Integer, ForeignKey("Sensor.id"))
    note = Column(String)
    status_id = Column(Integer, ForeignKey("LU_Status.id"))
    qc_id = Column(Integer, ForeignKey("QC.id"))
    public_release = Column(Boolean, default=False)
    data_source_id = Column(Integer, ForeignKey("LU_DataSource.id"))
    measuring_agency = Column(String)
    measured_by = Column(String)

    thing = relationship("Thing")
    observed_property = relationship("ObservedProperty")


class Sensor(Base):
    name = Column(String)
    manufacture = Column
    install_date = Column(DateTime)


class QC(Base):
    user = Column(String)
    timestamp = Column(DateTime)
    status = Column(Boolean)
    note = Column(String)


class LU(object):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    meaning = Column(String)


#
#
# class LU_AltitudeMethod(Base, LU):
#     pass
#
#
# class LU_CoordinateAccuracy(Base, LU):
#     pass
#
#
# class LU_DataReliability(Base, LU):
#     pass
#
#
# class LU_SiteType(Base, LU):
#     pass
#
#


class LU_CurrentUse(Base, LU):
    pass


class LU_MeasurementMethod(Base, LU):
    pass


class LU_Status(Base, LU):
    pass


class LU_Formation(Base, LU):
    pass


class LU_DataSource(Base, LU):
    pass


class LU_AquiferType(Base, LU):
    pass


class LU_AquiferClass(Base, LU):
    pass


#
# class Location(Base):
#     LocationId = Column(UUIDType(binary=False), primary_key=True)
#     DateCreated = Column(DateTime)
#     PointID = Column(String)
#     SiteNames = Column(String)
#     SiteID = Column(String)
#     # AlternateSiteID
#     # AlternateSiteID2
#     SiteDate = Column(DateTime)
#     DataReliability = Column(String, ForeignKey("LU_DataReliability.code"))
#     Confidential = Column(Boolean)
#     SiteType = Column(String, ForeignKey("LU_SiteType.code"))
#     WL_Continuous = Column(Boolean)
#     WL_Intermittent = Column(Boolean)
#     WaterQuality = Column(Boolean)
#     WaterFlow = Column(Boolean)
#     Hydraulic = Column(Boolean)
#     Subsurface = Column(Boolean)
#     WellorSpgNoData = Column(Boolean)
#     SubsurfaceType = Column(String)
#     Easting = Column(Integer)
#     Northing = Column(Integer)
#     UTMDatum = Column(String)
#     CoordinateNotes = Column(String)
#     Altitude = Column(Float)
#     AltitudeAccuracy = Column(Float)
#     AltitudeMethod = Column(String, ForeignKey("LU_AltitudeMethod.code"))
#     AltDatum = Column(String)
#     Latitude = Column(Float)
#     Longitude = Column(Float)
#     LatLonDatum = Column(String)
#     CoordinateAccuracy = Column(String, ForeignKey("LU_CoordinateAccuracy.code"))
#     CoordinateMethod = Column(String)
#     Township = Column(Integer)
#     TownshipDirection = Column(String)
#     Range = Column(Integer)
#     RangeDirection = Column(String)
#     SectionQuarters = Column(Float)
#     # SPX
#     # SPY
#     QuadName = Column(String)
#     County = Column(String)
#     State = Column(String)
#     LocationNotes = Column(String)
#     WLReportDeliver = Column(DateTime)
#     ChemistryReportDeliver = Column(DateTime)
#     WLReportNote = Column(String)
#     ChemistryReportNote = Column(String)
#     X_NAD83_Zone12 = Column(String)
#     Y_NAD83_Zone12 = Column(String)
#     projectname = Column(String)
#     USGSProjectID = Column(String)
#     # ObjectID
#     LatitudeDD = Column(Float)
#     LongitudeDD = Column(Float)
#     # SSMA_TimeStamp
#     PublicRelease = Column(Boolean)
#     # Geometry
#
#     altitude_method = relationship("LU_AltitudeMethod")
#     coordinate_accuracy = relationship("LU_CoordinateAccuracy")
#     data_reliability = relationship("LU_DataReliability")
#     site_type = relationship("LU_SiteType")
#
#     @property
#     def altitude_method_meaning(self):
#         return self.altitude_method.meaning
#
#     @property
#     def coordinate_accuracy_meaning(self):
#         try:
#             return self.coordinate_accuracy.meaning
#         except BaseException:
#             return ""
#
#     @property
#     def data_reliability_meaning(self):
#         return self.data_reliability.meaning
#
#     @property
#     def site_type_meaning(self):
#         try:
#             return self.site_type.meaning
#         except BaseException:
#             return ""
#
#
# class Chemistry(object):
#     SamplePtID = Column(UUIDType, primary_key=True)
#     SamplePointID = Column(String)
#     Analyte = Column(String)
#     Symbol = Column(String)
#     SampleValue = Column(Float)
#     Units = Column(String)
#     Uncertainty = Column(Float)
#     AnalysisMethod = Column(String)
#     AnalysisDate = Column(DateTime)
#     Notes = Column(String)
#     Volume = Column(Integer)
#     VolumeUnit = Column(String)
#     # OBJECTID
#     # GlobalID
#     AnalysesAgency = Column(String)
#     WCLab_ID = Column(String)
#
#
# class MajorChemistry(Base, Chemistry):
#     pass
#
#
# class MinorandTraceChemistry(Base, Chemistry):
#     pass
#
#
# class WaterLevelMixin(object):
#     WellID = Column(UUIDType, primary_key=True)
#     PointID = Column(String)
#     OBJECTID = Column(String)
#     DepthToWaterBGS = Column(Float)
#     # MeasurementMethod=Column(String, ForeignKey('LU_MeasurementMethod.code'))
#     # DataSource=Column(String, ForeignKey('LU_DataSource.code'))
#     MeasuringAgency = Column(String)
#
#     # @declared_attr
#     # def measurement_method(self):
#     #     return relationship("LU_MeasurementMethod")
#     #
#     # @declared_attr
#     # def data_source(self):
#     #     return relationship("LU_DataSource")
#     #
#     # @declared_attr
#     # def DataSource(self):
#     #     return Column(String, ForeignKey("LU_DataSource.code"))
#     #
#     # @declared_attr
#     # def MeasurementMethod(self):
#     #     return Column(String, ForeignKey("LU_MeasurementMethod.code"))
#
#     # @property
#     # def measurement_method_meaning(self):
#     #     return self.measurement_method.meaning
#     #
#     # @property
#     # def data_source_meaning(self):
#     #     return self.data_source.meaning
#
#
# class WaterLevels(Base, WaterLevelMixin):
#     DepthToWater = Column(Float)
#     LevelStatus = Column(String)
#     # DataQuality = Column(String, ForeignKey("LU_DataQuality.code"))
#     MPHeight = Column(Float)
#     MeasuredBy = Column(String)
#     SiteNotes = Column(String)
#     LevelStatement = Column(String)
#     PublicRelease = Column(Boolean)
#     DateMeasured = Column(Date)
#     TimeMeasured = Column(Time)
#     TimeDatum = Column(String)
#
#     # data_quality = relationship("LU_DataQuality")
#
#     @property
#     def data_quality_meaning(self):
#         return 'asdf'
#         # return self.data_quality.meaning
#
#     @property
#     def DateTimeMeasured(self):
#         dt = self.DateMeasured
#         if self.TimeMeasured:
#             dt = datetime.combine(self.DateMeasured, self.TimeMeasured)
#         else:
#             dt = datetime.fromordinal(dt.toordinal())
#         return dt
#
#
# class WaterLevelsContinuousMixin(WaterLevelMixin):
#     DateMeasured = Column(DateTime)
#
#     @property
#     def DateTimeMeasured(self):
#         return self.DateMeasured
#
#
# class WaterLevelsContinuous_Pressure(Base, WaterLevelsContinuousMixin):
#     TemperatureWater = Column(Float)
#     # WaterHead
#     # WaterHeadAdjusted
#     DepthToWaterBGS = Column(Float)
#     # MeasurementMethod
#     # DataSource
#     # MeasuringAgency
#     QCed = Column(Boolean)
#     Notes = Column(String)
#     Created = Column(DateTime)
#     Updated = Column(DateTime)
#     ProcessedBy = Column(String)
#     CheckedBy = Column(String)
#     conddl = Column("CONDDL (mS/cm)", Float)
#
#
# class WaterLevelsContinuous_Acoustic(Base, WaterLevelsContinuousMixin):
#     TemperatureAir = Column(Float)
#
#     Notes = Column(String)
#     SerialNo = Column(String)
#     # PreProcessDataField=Column()
#     ServerReceiptDate = Column(DateTime)
#     WellntelReadingType = Column(String)
#     SensorHgtAboveMP = Column(Float)
#     SpeakerToMicLength = Column(Integer)
#     PublicRelease = Column(Boolean)
#     Created = Column(DateTime)
#     EventID = Column(Integer)
#     ImportID = Column(UUIDType)
#
# # class Meter(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #     serial_year = Column(Integer)
# #     serial_case_diameter = Column(Integer)
# #     serial_id = Column(Integer)
# #
# #     # well = relationship('Well', back_populates='meter')
# #
# #     @property
# #     def serial_number(self):
# #         return f"{self.serial_year}-{self.serial_case_diameter}-{self.serial_id}"
# #
# #
# # class MeterHistory(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #
# #     well_id = Column(Integer, ForeignKey("Well.id"))
# #     meter_id = Column(Integer, ForeignKey("Meter.id"))
# #     timestamp = Column(DateTime, default=func.now())
# #     note = Column(LargeBinary)
# #
# #     meter = relationship("Meter", uselist=False)
# #
# #
# # class Well(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #
# #     township = Column(Integer)
# #     range = Column(Integer)
# #     section = Column(Integer)
# #     quarter = Column(Integer)
# #     half_quarter = Column(Integer)
# #     quarter_quarter = Column(Integer)
# #
# #     # latitude = Column(Float)
# #     # longitude = Column(Float)
# #
# #     geom = Column(Geometry("POINT"))
# #
# #     owner_id = Column(Integer, ForeignKey("Owner.id"))
# #     osepod = Column(String)
# #
# #     # meter = relationship('Meter', uselist=False, back_populates='well')
# #     owner = relationship("Owner", back_populates="wells")
# #     readings = relationship("Reading", back_populates="well")
# #
# #     meter_history = relationship("MeterHistory", uselist=False)
# #
# #     @property
# #     def latitude(self):
# #         return to_shape(self.geom).y
# #
# #     @property
# #     def longitude(self):
# #         return to_shape(self.geom).x
# #
# #     @property
# #     def location(self):
# #         return f"{self.township}.{self.range}.{self.section}.{self.quarter}.{self.half_quarter}"
# #
# #
# # class Reading(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     value = Column(Float)
# #     eread = Column(String)
# #     repair = Column(LargeBinary)
# #     timestamp = Column(DateTime)
# #     well_id = Column(Integer, ForeignKey("Well.id"))
# #
# #     well = relationship("Well", back_populates="readings")
# #
# #
# # class Owner(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #
# #     wells = relationship("Well", back_populates="owner")
# #
# #
# # class Worker(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #
# #
# # class MeterStatusLU(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String)
# #     description = Column(String)
# #
# #
# # class Repair(Base):
# #     id = Column(Integer, primary_key=True, index=True)
# #     # meter_id = Column(Integer, ForeignKey('metertbl.id'))
# #     well_id = Column(Integer, ForeignKey("Well.id"))
# #     worker_id = Column(Integer, ForeignKey("Worker.id"))
# #
# #     timestamp = Column(DateTime, default=func.now())
# #     h2o_read = Column(Float)
# #     e_read = Column(String)
# #     new_read = Column(String)
# #     repair_description = Column(LargeBinary)
# #     note = Column(LargeBinary)
# #     meter_status_id = Column(Integer, ForeignKey("MeterStatusLU.id"))  # pok, np, piro
# #     preventative_maintenance = Column(String)
# #
# #     well = relationship("Well", uselist=False)
# #     repair_by = relationship("Worker", uselist=False)
# #     meter_status = relationship("MeterStatusLU", uselist=False)
# #
# #     @property
# #     def well_name(self):
# #         return self.well.name
# #
# #     @property
# #     def well_location(self):
# #         return self.well.location
# #
# #     @property
# #     def meter_serial_number(self):
# #         return self.well.meter_history.meter.serial_number
# #
# #     @property
# #     def meter_status_name(self):
# #         return self.meter_status.name
# #
# #     @property
# #     def worker(self):
# #         return self.repair_by.name
# #
# #     @worker.setter
# #     def worker(self, v):
# #         self.repair_by.id
# #

# ============= EOF =============================================
