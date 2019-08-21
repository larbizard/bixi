import pandas as pd
import requests
import json
from time import sleep
import psycopg2
from datetime import datetime
from requests.exceptions import ConnectionError


#bixi_201904 = pd.read_csv('data/OD_2019-04.csv')
#bixi_201905 = pd.read_csv('data/OD_2019-05.csv')

#stations2019 = pd.read_csv('data/Stations_2019.csv')

#print(bixi_201904.query('start_station_code==6001 & start_date<="2019-04-14 23:59:59"'))

#bixi_api = requests.get('https://api-core.bixi.com/gbfs/en/station_information.json')
#station_information = bixi_api.json()

#data['data']['stations'][0]['station_id']
#data['data']['stations'][0]['capacity']

# Let's suppose that the first bike was rented on 2019-04-14 07:55:22 at station 6001
# 10    6001            Métro Champ-de-Mars (Viger / Sanguinet)  45.510351 -73.556508

#for station in station_information['data']['stations']:
#    print('"s' + station['station_id'] + '"' + ' INT,')


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="bixi_db", user="bixi", password="bixi")
        cur = conn.cursor()

        bixi_api = requests.get('https://api-core.bixi.com/gbfs/en/station_status.json')

        if bixi_api != "No response":
            station_status = bixi_api.json()

            occupation_data = {}

            occupation_data['upd_timestamp'] = datetime.utcfromtimestamp(station_status['last_updated'])\
                .strftime("%Y-%m-%d %H:%M:%S")
            for station in station_status['data']['stations']:
                occupation_data['s' + station['station_id']] = station['num_bikes_available']


            placeholders = ', '.join(['%s'] * len(occupation_data))
            columns = ', '.join(occupation_data.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('occupation', columns, placeholders)

            cur.execute(sql, list(occupation_data.values()))
            conn.commit()

            print(datetime.utcfromtimestamp(station_status['last_updated']).strftime("%Y-%m-%d %H:%M:%S"))
            print(json.dumps(occupation_data, indent=4, sort_keys=True))

        cur.close()
        conn.close()

        sleep(300)

    except ConnectionError as e:  # This is the correct syntax
        print(e)
        bixi_api = "No response"



