# coding=utf-8

import urllib2, json, datetime

api_key = "5af1beca494712ed38d313714d4caff6"
query_url = "https://www.mvg.de/fahrinfo/api/location/query?q="
departure_url = "https://www.mvg.de/fahrinfo/api/departure/"
departure_url_postfix = "?footway=0"


class Station:
    """
        Gives you an object to acess current departure times from mvg.de

        Either give it an exact station_name (like "Hauptbahnhof") or a station_id.
    """

    def __init__(self, station_name="", station_id=0):
        if station_name:
            self.station_id = self._query_station_name(station_name)
        elif station_id:
            self.station_id = station_id
        else:
            raise ValueError("Please provide a 'station_name' or 'station_id'")

    def _query_station_name(self, station_name):
        """
            Gives the station_id for the given station_name.
            If more than one station match, the first result is given.
            None is returned if no match was found.
        """
        url = query_url + station_name
        opener = urllib2.build_opener()
        opener.addheaders = [('X-MVG-Authorization-Key', '5af1beca494712ed38d313714d4caff6')]
        response = opener.open(url)
        results = json.loads(response.read())
        for result in results['locations']:
            if result['type'] == 'station':
                return result['id']

    def get_departures(self, in_minutes=False):
    """
        Fetches the departures and returns them as an array.
        By default, the times are given in Unix time.
        With in_minutes=True, the times are replaced with the time difference in minutes.
    """
        url = departure_url + str(self.station_id) + departure_url_postfix
        opener = urllib2.build_opener()
        opener.addheaders = [('X-MVG-Authorization-Key', '5af1beca494712ed38d313714d4caff6')]
        response = opener.open(url)
        departures = json.loads(response.read())['departures']
        for departure in departures:
            # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
            # Here, we convert it to a standard unix timestamp.
            departure['departureTime'] = departure['departureTime'] / 1000
            if in_minutes:
                time = datetime.datetime.fromtimestamp(departure['departureTime'])
                relative_time = time - datetime.datetime.now()
                departure['departureTime'] = relative_time.seconds // 60
        return departures

obersendling = Station(station_name="Siemens")
departures = obersendling.get_departures(in_minutes=True)
print departures
