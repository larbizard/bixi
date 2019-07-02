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

    def __init__(self):
        return name

    def get_station_information(self):
        return requests.get('https://api-core.bixi.com/gbfs/en/station_information.json').json()

    def get_stations_status(self):
        return requests.get('https://api-core.bixi.com/gbfs/en/station_status.json').json()

    def get_week_days_in_year(self, year, day):
        pd.date_range(start=str(year), end=str(year + 1), freq=day).strftime('%Y-%m-%d').tolist()


    def get_station_occupancy(self, station_short_name, year, day, hour):
        conn = psycopg2.connect(host="localhost", database="bixi_db", user="bixi", password="bixi")
        cur = conn.cursor()

        station_status = get_stations_status()

        occupation_data = {}

        occupation_data['upd_timestamp'] = station_status['last_updated']
        for station in station_status['data']['stations']:
            occupation_data['s' + station['station_id']] = station['num_bikes_available']

        station_id = 's' + station_id
        placeholders = ', '.join(['%s'] * len(occupation_data))
        columns = ', '.join(occupation_data.keys())

        for d in get_week_days_in_year(year, day):
            sql = "SELECT %s FROM %s WHERE upd_timestamp like %s %s" % (station_id, 'occupation', d, hour)

        cur.close()
        conn.close()
