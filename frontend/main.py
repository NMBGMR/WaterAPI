import os

import requests
from flask import Flask, render_template, Markup, redirect

from frontend import WL_DISCLAIMER
from frontend.plotting import make_hydrograph

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/api/v1/docs")


@app.route("/map")
def map():
    map_cfg = {
        "center_lat": 33.5,
        "center_lon": -104.5,
        "zoom": 7,
        "base_api_url": os.environ.get("BASE_API_URL", "http://localhost/api/v1/"),
    }

    return render_template("index.html", disclaimer=WL_DISCLAIMER, map_cfg=map_cfg)


@app.route("/entry")
def entry():
    return render_template("entry.html")


#
# @app.route("/waterlevels/<string:pointid>")
# def waterlevels(pointid):
#     acs = []
#     resp = requests.get(
#         f"http://host.docker.internal/api/v1/waterlevelspressure?pointid={pointid}"
#     )
#     pt = resp.json()
#
#     resp = requests.get(
#         f"http://host.docker.internal/api/v1/waterlevels?pointid={pointid}"
#     )
#     manual = resp.json()
#     js, div = make_hydrograph(pt, acs, manual, pointid)
#
#     disclaimer = Markup(WL_DISCLAIMER)
#
#     datanote = Markup(
#         """Please use all data with caution and awareness of their limitations. There are locations with duplicate data
#         or conflicting data at the same locations that have not been resolved. Data displayed here are not dynamically
#         updated (as of June 2016), and locations may not be accurate. Well depths may not be accurate or may have changed,
#         this is especially true for data derived from historical publications (noted in data source fields). Data providers
#         (NMED, NMBGMR, or USGS) shall not be liable for any activity involving these data."""
#     )
#
#     return render_template(
#         "waterlevels.html",
#         figJS=js,
#         figDiv=div,
#         pointid=pointid,
#         datanote=datanote,
#         disclaimer=disclaimer,
#         base_api_url=os.environ.get('BASE_API_URL', 'http://localhost/api/v1'),
#     )


# DESCRIPTIONS = ['Start', 'Getting More Data', 'Writing to CSV', 'JSON Schema']
#
# @app.route("/tutorial/<int:page>")
# def tutorial(page):
#     page_description = DESCRIPTIONS[page]
#
#     return render_template(f'tutorial{page}.html',
#                            page=page, page_description=page_description)
#
# @app.route("/qgis")
# def qgis():
#     return render_template("qgis_example.html")
#
#
# @app.route("/browser_examples")
# def examples():
#     return render_template('browser_examples.html')
#
# @app.route("/scoreboard")
# def scoreboard():
#     resp = requests.get('http://developer.newmexicowaterdata.org/api/v1/st2_report')
#     sb = {}
#     if resp.status_code == 200:
#         sb = resp.json()
#     return render_template("scoreboard.html", sb=sb)
#
#
# @app.route("/")
# def help_link():
#     return render_template('index.html')
