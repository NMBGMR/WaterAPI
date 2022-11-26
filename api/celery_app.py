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
from celery import Celery

from api.setup_db import copy_nm_aquifer

veg = Celery(
    "worker",
    broker_url="redis://redis:6379",
    result_backend="redis://redis:6379",
)


@veg.task()
def copy_nm_aquifer_task(request):
    copy_nm_aquifer()


# ============= EOF =============================================
