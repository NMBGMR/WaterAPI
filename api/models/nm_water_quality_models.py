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
    Date,
    Time,
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

    symbol_tag = None
    value_tag = None

    @property
    def value(self):
        return getattr(self, self.value_tag)

    @property
    def symbol(self):
        tag = self.symbol_tag
        if tag is None:
            tag = self.value_tag

        return getattr(self, f"{tag}_Symbol")


class WQ_Arsenic(Base, ElementMixin):
    Arsenic = Column(Float)
    Arsenic_Symbol = Column(String)
    value_tag = "Arsenic"


class WQ_Bicarbonate(Base, ElementMixin):
    HCO3 = Column(Float)
    HCO3_Symbol = Column(String)
    value_tag = "HCO3"


class WQ_Chlorine(Base, ElementMixin):
    Cl = Column(Float)
    Cl_Symbol = Column(String)
    value_tag = "Cl"


class WQ_Calcium(Base, ElementMixin):
    Ca = Column(Float)
    Ca_Symbol = Column(String)
    value_tag = "Ca"


class WQ_Fluoride(Base, ElementMixin):
    F = Column(Float)
    F_Symbol = Column(String)
    value_tag = "F"


class WQ_Magnesium(Base, ElementMixin):
    Mg = Column(Float)
    Mg_Symbol = Column(String)
    value_tag = "Mg"


class WQ_Sodium(Base, ElementMixin):
    Na = Column(Float)
    Na_Symbol = Column(String)
    value_tag = "Na"


class WQ_Sulfate(Base, ElementMixin):
    SO4 = Column(Float)
    SO4_Symbol = Column(String)
    value_tag = "SO4"


class WQ_TDS(Base, ElementMixin):
    TDS = Column(Float)
    TDS_Symbol = Column(String)
    value_tag = "TDS"


class WQ_Uranium(Base, ElementMixin):
    U = Column(Float)
    Uranium_Symbol = Column(String)
    value_tag = "U"
    symbol_tag = "Uranium"


class WQ_Specific_Conductance(Base, ElementMixin):
    CONDLAB = Column(Float)
    CONDLAB_Symbol = Column(String)
    value_tag = "CONDLAB"


# ============= EOF =============================================
