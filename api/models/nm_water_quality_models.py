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
from typing import Any
from sqlalchemy_utils import UUIDType
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
    Date,Time
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class ElementMixin(object):
    POINT_ID = Column(String)
    CollectionDate = Column(DateTime, primary_key=True)
    HistoricDate = Column(Integer)
    Latitude = Column(Float)
    Longitude = Column(Float)
    WellDepth = Column(Float)
    DataSource = Column(String)
    DataSourceInfo = Column(String)
    # GeoLocation
    @property
    def value(self):
        return getattr(self, self.value_tag)

    @property
    def symbol(self):
        return getattr(self, f"{self.value_tag}_Symbol")

class WQ_Arsenic(Base, ElementMixin):
    Arsenic = Column(Float)
    Arsenic_Symbol = Column(String)
    value_tag = 'Arsenic'


class WQ_Bicarbonate(Base, ElementMixin):
    HCO3 = Column(Float)
    HCO3_Symbol = Column(String)
    value_tag = 'HCO3'
# ============= EOF =============================================
