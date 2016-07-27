from mvg import Station

obersendling = Station("Obersendling")
departures = obersendling.get_departures()

for departure in departures:
    print departure['product'] + departure['label'] + "\t" + departure['destination'] + "\t" + str(departure['departureTimeMinutes'])
