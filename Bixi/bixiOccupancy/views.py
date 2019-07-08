from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import BixiStationOccupancy


def index(request):
    day = 'W-TUE'
    hour = 15
    BixiStationOccupancyInstance = BixiStationOccupancy('6001')
    BixiStationOccupancyInstance.get_station_occupancy(2019, day, hour)
    message = 'The average occupation for station ' + BixiStationOccupancyInstance.name \
              +' on '+ day +' at ' + str(hour) + ' is: ' + str(round(100-BixiStationOccupancyInstance.occupation * 100, 2)) + u'\u0025'

    context = {
        "title": "Bixi Occupancy",
        "message": message
    }

    return render(request, "bixiOccupancy/index.html", context)
