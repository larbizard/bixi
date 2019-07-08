from BixiStationOccupancy import BixiStationOccupancy


def run():
    day = 'W-WED'
    hour = 14
    BixiStationOccupancyInstance = BixiStationOccupancy('6001')
    BixiStationOccupancyInstance.get_station_occupancy(2019, day, hour)
    print('The average occupation for station %s on %s at %s is: %s'
          %(BixiStationOccupancyInstance.name,
          day,
          hour,
           round(BixiStationOccupancyInstance.occupation * 100, 2)) + u'\u0025')
run()
