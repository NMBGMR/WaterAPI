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
from fastapi_pagination import add_pagination, Page, paginate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.routes import get_waterdb
from api.reports import point_id as report_point_id


router = APIRouter()
@router.get('/point_id_report/{point_id}', tags=["Reports"])
def read_point_id_report(point_id: str,
                         format: str= "pdf",
                         db: Session = Depends(get_waterdb)):
    if format=='pdf':
        # make pdf report
        report = report_point_id.make_pdf_report(db, point_id)
    else:
        # make json report
        report = report_point_id.make_json_report(db, point_id)
    return report
# ============= EOF =============================================
