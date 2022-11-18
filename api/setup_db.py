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

from api.models.wl_models import Base, Location, Well, ObservedProperty, WellMeasurement
from api.session import waterdbengine, WATERDB


def setup_db():
    if int(os.environ["DATABASE_DEV"]):
        Base.metadata.drop_all(bind=waterdbengine)
        Base.metadata.create_all(bind=waterdbengine)

        db = WATERDB()
        db.add(Location(PointID="JR-001"))
        db.add(Location(PointID="JR-002"))
        db.commit()
        db.add(Well(location_id=1))
        db.add(Well(location_id=2))
        db.add(ObservedProperty(name="DepthToWaterBGS"))
        db.add(ObservedProperty(name="WellTemperature"))
        db.commit()
        db.add(WellMeasurement(well_id=1, value=10, observed_property_id=1))
        db.add(WellMeasurement(well_id=2, value=131, observed_property_id=1))

        db.add(WellMeasurement(well_id=1, value=103, observed_property_id=2))
        db.commit()
        db.close()


# ============= EOF =============================================
