import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd

import requests

import psycopg2
from datetime import datetime
from datetime import date, timedelta


class BixiStationOccupation:

    name = 'default'
    station_id = '0'
    short_name = '0000'
    lat = 43
    lon = -73
    capacity = 10
    occupation = 0
    year = 2019
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
    # Alias
    # Description
    # W - SUN
    # weekly
    # frequency(Sundays).Same as ‘W’
    # W - MON
    # weekly
    # frequency(Mondays)
    # W - TUE
    # weekly
    # frequency(Tuesdays)
    # W - WED
    # weekly
    # frequency(Wednesdays)
    # W - THU
    # weekly
    # frequency(Thursdays)
    # W - FRI
    # weekly
    # frequency(Fridays)
    # W - SAT
    # weekly
    # frequency(Saturdays)
    day = 'W-SUN'

    def __init__(self, station_short_name):
        for s in self.get_station_information()['data']['stations']:
            if s['short_name'] == station_short_name:
                self.station_id = 's' + s['station_id']
                self.capacity = s['capacity']
                self.name = s['name']
                break

    def get_station_information(self):
        return requests.get('https://api-core.bixi.com/gbfs/en/station_information.json').json()

    def get_stations_status(self):
        return requests.get('https://api-core.bixi.com/gbfs/en/station_status.json').json()

    def get_week_days_in_year(self, year, day):
        return pd.date_range(start=str(year), end=str(year + 1), freq=day).strftime('%Y-%m-%d').tolist()

    def get_station_occupancy(self, year, day, hour):
        conn = psycopg2.connect(host="localhost", database="bixi_db", user="bixi", password="bixi")
        cur = conn.cursor()

        records = []

        for d in self.get_week_days_in_year(year, day):
            date1 = datetime.strptime(d + ' ' + str(hour), '%Y-%m-%d %H')
            date2 = datetime.strptime(d + ' ' + str(hour+1), '%Y-%m-%d %H')
            sql = "SELECT %s FROM %s WHERE upd_timestamp >= %s AND upd_timestamp < %s" \
                  % (self.station_id, 'occupation', "'%" + date1.strftime('%Y-%m-%d %H:%M:%S') + "%'"
                     , "'%" + date2.strftime('%Y-%m-%d %H:%M:%S') + "%'")
            cur.execute(sql)
            records = records + cur.fetchall()

        for row in records:
            self.occupation = self.occupation + row[0]/self.capacity

        cur.close()
        conn.close()

        self.occupation = self.occupation/len(records)

