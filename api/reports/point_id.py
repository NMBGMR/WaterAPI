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
import io
import os
from io import StringIO
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Frame,
    PageTemplate,
    Image,
    XBox,
)
from reportlab.lib.units import inch

from api.models.wl_models import Location, Well
from api.schemas import wl_schemas


def make_json_data(db, point_id):
    q = db.query(Well).join(Location).filter(Location.point_id == point_id)
    dbwell = q.first()

    dbloc = dbwell.location
    dbwc = dbwell.well_construction

    loc = wl_schemas.Location.from_orm(dbloc)
    well = wl_schemas.Well.from_orm(dbwell)
    wc = wl_schemas.WellConstruction.from_orm(dbwc)

    data = {"location": loc.dict(), "well": well.dict(), "well_construction": wc.dict()}

    return data


def human(k):
    args = k.split("_")

    def prep(a):
        a = a.capitalize()
        if a == "Ose":
            a = "OSE"
        elif a == "Id":
            a = "ID"
        return a

    args = [prep(a) for a in args]
    return " ".join(args)


def make_table(elements, rows, title):
    tdata = []
    for k, v in rows:
        k = human(k)

        p = Paragraph(f"<strong>{k}</strong>")
        tdata.append([p, str(v or "")])

    style = ParagraphStyle(name="Normal", fontSize=14)

    elements.append(Paragraph(f"<strong>{title}</strong>", style=style))
    elements.append(Spacer(1, 5))

    t = Table(tdata)
    t.hAlign = "LEFT"
    ts = TableStyle(
        [
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
        ]
    )
    t.setStyle(ts)
    elements.append(t)
    elements.append(Spacer(1, 20))


def make_pdf_report(db, point_id):
    header_height = 1.5 * inch
    data = make_json_data(db, point_id)

    elements = []
    p = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "newmexicobureauofgeologyandmineralresources.jpeg",
    )
    elements.append(
        Image(p, width=header_height * 0.9 * 1.25, height=header_height - 15)
    )
    # Initialise the simple document template
    path = f"report.{point_id}.pdf"
    doc = SimpleDocTemplate(
        path,
        page_size=letter,
        bottomMargin=0.4 * inch,
        topMargin=0.4 * inch,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
    )

    style = ParagraphStyle(name="Normal", fontSize=14)
    pp = Paragraph(f"<strong>PointID: {point_id}</strong>", style=style)
    elements.append(pp)
    elements.append(Spacer(1, 12))

    loc = data["location"]
    rows = [
        ("Latitude", loc["latitude"]),
        ("Longitude", loc["longitude"]),
        ("County", loc["county"]),
    ]
    make_table(elements, rows, "Location")

    rows = [(k, v) for k, v in data["well"].items() if k != "well_construction"]
    make_table(elements, rows, "Well")
    make_table(elements, data["well_construction"].items(), "Well Construction")
    # elements.append(Spacer(1,inch*3))

    p = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fnewmexicobureauofgeologyandmineralresources.jpeg",
    )
    if os.path.isfile(p):
        elements.append(Image(p, width=inch * 3, height=inch * 2))
    else:
        elements.append(XBox(width=inch * 3, height=inch * 2))

    column_height = letter[1] - header_height - 0.4 * inch
    y = doc.height - column_height - header_height + 0.4 * inch

    hf = Frame(
        doc.leftMargin,
        doc.height - header_height + 0.4 * inch,
        inch * 3,
        header_height,
        id="header",
    )

    lf = Frame(
        doc.leftMargin, y, doc.width / 2, column_height, id="col1", showBoundary=1
    )
    rf = Frame(
        doc.width / 2 + doc.leftMargin,
        y,
        doc.width / 2,
        column_height,
        id="col2",
        showBoundary=1,
    )

    template = PageTemplate(id="twoColumn", frames=[hf, lf, rf])
    doc.addPageTemplates([template])
    # build PDF using the data
    doc.build(elements)

    return path


# ============= EOF =============================================
