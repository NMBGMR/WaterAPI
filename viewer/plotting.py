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
from bokeh.embed import components
from bokeh.models import (
    NumeralTickFormatter,
    ColumnDataSource,
    HoverTool,
    BoxZoomTool,
    ResetTool,
    WheelZoomTool,
    PanTool,
    Range1d,
)
from bokeh.plotting import figure
from bokeh.resources import CDN
from datetime import datetime


def make_datetime_figure(
    xlabel="Date", ylabel="Value", yformat="0.0", plot_width=1400, plot_height=700, **kw
):
    f = figure(
        # outer_width=plot_width, outer_height=plot_height,
        x_axis_type="datetime",
        **kw
    )
    f.outline_line_width = 2
    f.outline_line_alpha = 0.3
    f.outline_line_color = "black"
    f.background_fill_color = "beige"
    f.xaxis.axis_label = xlabel
    f.yaxis.axis_label = ylabel

    if yformat:
        f.yaxis[0].formatter = NumeralTickFormatter(format=yformat)

    return f


def set_min_limits(fig, ys, threshold=1):
    yma, ymi = max(ys), min(ys)
    dev = abs(yma - ymi)
    pad = threshold / 2.0
    if dev < threshold:
        center = ymi + dev / 2.0

        fig.y_range = Range1d(center - pad, center + pad)


def extractxy(records):
    records = sorted(records, key=lambda x: x["DateTimeMeasured"])
    return zip(
        *(
            (
                datetime.strptime(r["DateTimeMeasured"], "%Y-%m-%dT%H:%M:%S"),
                -r["DepthToWaterBGS"],
            )
            for r in records
            if r["DepthToWaterBGS"]
        )
    )


def make_hydrograph(pt, acs, manual, pointid):
    valid = False
    fig = make_datetime_figure(
        title="Hydrograph {}".format(pointid),
        ylabel="Depth to Water (ft Below Ground Surface)",
    )
    display_line = True

    if pt and len(pt) > 1:
        # xs, ys = zip(*((datetime.strptime(r[0], '%Y-%m-%d'), -r[1]) for r in pt))
        # xs, ys = zip(*((r['DateTimeMeasured'], -r[1]) for r in pt))
        xs, ys = extractxy(pt)
        set_min_limits(fig, ys)

        # plot qced data
        ps = [p for p in pt if p["QCed"]]
        # print(ps)
        if ps:
            xs, ys = extractxy(ps)
            # xs, ys = zip(*((r['DateTimeMeasured'], -r['DepthToWaterBGS']) for r in ps))
            print(xs, ys)
            # fig.line(xs, ys, legend=ps[0][3])
            fig.line(xs, ys)
            valid = True
            display_line = False

        # plot non qced
        ps = [p for p in pt if not p["QCed"]]
        if ps:
            xs, ys = extractxy(ps)
            # xs, ys = zip(*((r['DateTimeMeasured'], -r['DepthToWaterBGS']) for r in ps))
            # fig.line(xs, ys, line_color='red', legend='Non QCed {}'.format(ps[0][3]))
            fig.line(xs, ys, line_color="red")

            valid = True
            display_line = False

    if acs and len(acs) > 1:
        xs, ys = zip(*((r[0], -r[1]) for r in acs))
        fig.line(xs, ys, legend=acs[0][3])
        set_min_limits(fig, ys)
        valid = True
        display_line = False

    if manual and (len(manual) > 1 or valid):
        xs, ys = extractxy(manual)
        # manual = sorted(manual, key=lambda x: x['DateTimeMeasured'])
        # xs, ys = zip(*((datetime.strptime(r['DateTimeMeasured'],
        #                                   '%Y-%m-%dT%H:%M:%S'), -r['DepthToWaterBGS'])
        #                for r in manual if r['DepthToWaterBGS']))
        if display_line:
            fig.line(xs, ys, line_color="orange", line_width=2)
        fig.circle(xs, ys, fill_color="yellow", size=8)
        valid = True

    if valid:
        return components(fig, CDN)
    else:
        return None, None


# ============= EOF =============================================
