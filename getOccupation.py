from BixiStationOccupation import BixiStationOccupation


def run():
    day = 'W-WED'
    hour = 14
    bixiStationOccupation = BixiStationOccupation('6001')
    bixiStationOccupation.get_station_occupancy(2019, day, hour)
    print('The average occupation for station %s on %s at %s is: %s'
          %(bixiStationOccupation.name,
          day,
          hour,
           round(bixiStationOccupation.occupation * 100, 2)) + u'\u0025')
run()
