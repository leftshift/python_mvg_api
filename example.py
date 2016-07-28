from mvg import *

obersendling = Station("Obersendling")
departures = obersendling.get_departures()

for departure in departures:
    print departure['product'] + departure['label'] + "\t" + departure['destination'] + "\t" + str(departure['departureTimeMinutes'])

print get_nearby_stations(48.0933264, 11.537161699999999)
