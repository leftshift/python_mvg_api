# coding=utf-8

import urllib2, json, datetime

api_key = "5af1beca494712ed38d313714d4caff6"
query_url = "https://www.mvg.de/fahrinfo/api/location/query?q="
departure_url = "https://www.mvg.de/fahrinfo/api/departure/"
departure_url_postfix = "?footway=0"
nearby_url = "https://www.mvg.de/fahrinfo/api/location/nearby"

def _perform_api_request(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('X-MVG-Authorization-Key', api_key)]
    response = opener.open(url)
    return json.loads(response.read())


def get_nearby_stations(lat, log):
    if lat == 0 or log == 0:
        return None

    if not (isinstance(lat, float) and isinstance(log, float)):
        raise TypeError()

    url = nearby_url + "?latitude=%f&longitude=%f" % (lat, log)

    results = _perform_api_request(url)
    return results['locations']

def get_id_for_station(station_name):
    """
    Gives the station_id for the given station_name.
    If more than one station match, the first result is given.
    None is returned if no match was found.
    """
    station = get_station(station_name)
    return station['id']

def get_station(station):
    if isinstance(station, int):
        url = query_url + str(station)
    else:
        url = query_url + urllib2.quote(station)
    results = _perform_api_request(url)

    for result in results['locations']:
        if result['type'] == 'station':
            return result

class Station:
    """
        Gives you an object to acess current departure times from mvg.de

        Either give it an exact station name (like "Hauptbahnhof") or a station_id.
    """

    def __init__(self, station):
        if isinstance(station, str) or isinstance(station, unicode):
            self.station_id = get_id_for_station(station)
            if self.station_id == None:
                raise NameError("No matching station found")
        elif isinstance(station, int):
            self.station_id = station
        else:
            raise ValueError("Please provide a Station Name or ID")

    def get_departures(self):
        """
        Fetches the departures and returns them as an array.
        By default, the times are given in Unix time.
        Also, the relative time in minutes is given in departureTimeMinutes
        """
        url = departure_url + str(self.station_id) + departure_url_postfix
        departures = _perform_api_request(url)['departures']
        for departure in departures:
            # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
            # Here, we convert it to a standard unix timestamp.
            departure['departureTime'] = departure['departureTime'] / 1000

            time = datetime.datetime.fromtimestamp(departure['departureTime'])
            relative_time = time - datetime.datetime.now()
            departure[u'departureTimeMinutes'] = relative_time.seconds // 60
        return departures
