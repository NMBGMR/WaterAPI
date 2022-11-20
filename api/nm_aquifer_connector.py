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


def get_gw_locations(cursor, public_release='true'):
    def func():
        i = 0
        while 1:
            sql = f"""select * from dbo.Location 
--             where PointID like 'AB-%'
            where PublicRelease=(%s) and SiteType='GW'
            order by PointID
            offset {i*100} rows fetch next 100 rows only
            """
            print(sql, public_release)
            cursor.execute(sql, public_release)
            records = cursor.fetchall()
            if not records:
                break
            yield from records

            i += 1

    return func()


def get_screens(cursor, pointid):
    sql = "select * from dbo.WellScreens where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_welldata(cursor, pointid):
    sql = "select * from dbo.WellData where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_projects(cursor):
    sql = "select * from dbo.Projects"
    return fetch(cursor, sql)


def get_associated_projects(cursor, pointid):
    sql = "select * from dbo.ProjectLocations where PointID=%s"
    return fetch(cursor, sql, pointid)


def get_manual_water_levels(cursor, pointid):
    sql = """select (CASE
     WHEN TimeMeasured is NULL 
     then CONVERT(DateTime, DateMeasured) 
        else
       CONVERT(DateTime, DateMeasured) + CONVERT(DateTime, TimeMeasured) 
       end) as DateTimeMeasured, * from dbo.WaterLevels where PointID=%s order by DateMeasured"""
    return fetch(cursor, sql, pointid)


def get_pressure_water_levels(cursor, pointid):
    sql = """select * from dbo.WaterLevelsContinuous_Pressure
    where PointID=%s order by DateMeasured"""
    return fetch(cursor, sql, pointid)


def get_acoustic_water_levels(cursor, pointid):
    sql = """select * from dbo.WaterLevelsContinuous_Acoustic
        where PointID=%s order by DateMeasured"""
    return fetch(cursor, sql, pointid)


def fetch(cursor, sql, *args):
    cursor.execute(sql, *args)
    return cursor.fetchall()


def get_lookup_by_name(dest, table, name):
    q = dest.query(table).filter(table.name == name)
    try:
        return q.first().id
    except AttributeError:
        pass


# ============= EOF =============================================
