# coding=utf-8

from mvg import *

obersendling = Station("Obersendling")
departures = obersendling.get_departures()

for departure in departures:
    print(departure['product'] + departure['label'] + "\t" + departure['destination'] + "\t" + unicode(departure['departureTimeMinutes']))

print(get_nearby_stations(48.0933264, 11.537161699999999))

print(get_route(1, 2, max_time_to_dest=12, max_time_to_start=15))
