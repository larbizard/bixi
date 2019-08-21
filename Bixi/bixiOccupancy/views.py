from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import BixiStationOccupancy
import json


def index(request):
    if request.method == 'POST':

        year = request.POST.get('year')
        day = request.POST.get('day')
        hour = request.POST.get('hour')
        short_name = request.POST.get('short_name')

        response_data = {}

        try:

            #import pdb
            #pdb.set_trace()

            BixiStationOccupancyInstance = BixiStationOccupancy(short_name)
            BixiStationOccupancyInstance.get_station_occupancy(year, day, hour)

            response_data['result'] = {
                "name": BixiStationOccupancyInstance.name,
                "occupancy": round(100 - BixiStationOccupancyInstance.occupation * 100, 2)
            }

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        except:
            return HttpResponse(
                json.dumps({"Error": "No data found"}),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
