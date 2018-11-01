# coding=utf-8

from mvg_api import *

departures = get_departures_by_name("Obersendling")

for departure in departures:
    print(departure['product'] + departure['label'] + "\t" + departure['destination'] + "\t" + str(departure['departureTimeMinutes']))

print(get_nearby_stations(48.0933264, 11.537161699999999))

print(get_route((48.1267, 11.62009), 2, max_walk_time_to_dest=12, max_walk_time_to_start=15))
