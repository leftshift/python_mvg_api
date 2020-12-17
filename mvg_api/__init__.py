# coding=utf-8

import requests
import datetime
from time import mktime

query_url_name = "https://www.mvg.de/api/fahrinfo/location/queryWeb?q={name}"  # for station names
query_url_id = "https://www.mvg.de/api/fahrinfo/location/query?q={id}"  # for station ids
departure_url = "https://www.mvg.de/api/fahrinfo/departure/{id}?footway={offset}"
nearby_url = "https://www.mvg.de/api/fahrinfo/location/nearby?latitude={lat}&longitude={lon}"
routing_url = "https://www.mvg.de/api/fahrinfo/routing/?"
interruptions_url = "https://www.mvg.de/.rest/betriebsaenderungen/api/interruptions"
id_prefix = "de:09162:"


class ApiError(Exception):
    """
    Some error was returned by the mvg api when handling the request.
    :ivar code: status code returned by the API
    :ivar reason: response given by the api (optional)
    """
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason

    def __str__(self):
        out = "Got status code {}".format(self.code)
        if self.reason:
            out += " with response {}".format(self.reason)
        return out


def _convert_id(old_id: int) -> str:
    return id_prefix + str(old_id)


def _station_sanity_check(id:str):
    """
    New ID format has these specifications:
    starts with de
    has two : (checked with split)
    second and third field is integer (not checked)
    :param id: station id to be checked
    :return: Boolean on id sanity
    """
    split_id = id.split(":")
    if not len(split_id)==3:
        return False
    if not split_id[0]=='de':
        return False
    return True


def _perform_api_request(url):
    resp = requests.get(
            url,
            headers={
                'User-Agent': 'python-mvg-api/1 (+https://github.com/leftshift/python_mvg_api)',
                'Accept': 'application/json'
                }
            )
    if not resp.ok:
        try:
            raise ApiError(resp.status_code, resp.json())
        except ValueError:
            raise ApiError(resp.status_code)
    return resp.json()


def _convert_time(time):
    """Converts unix time in milliseconds to datetime or the other way around

    Parameters
    ----------
    time : int or datetime
        Unix timestamp (in milliseconds, like timestamp * 1000) or datetime.

    Returns
    -------
    int or datetime
        The opposite of the input.
    """
    if isinstance(time, datetime.datetime):
        return int(mktime(time.timetuple()))*1000
    else:
        timestamp = time / 1000
        return datetime.datetime.fromtimestamp(timestamp)


def get_nearby_stations(lat, lon):
    """Stations nearby the given location.

    Parameters
    ----------
    lat : float
        Latitude
    lon : float
         and longitude of the desired location.


    Returns a list which is formated in this fassion::

        [
            {
                'type': 'station',
                'latitude': 48.12046,
                'longitude': 11.61869,
                'id': 'de:09162:1060',
                'place': 'München',
                'name': 'Innsbrucker Ring',
                'hasLiveData': True,
                'hasZoomData': True,
                'products': ['UBAHN'],
                'aliases': 'Muenchen Munchen',
                'link': 'IR',
                'lines': {
                    'tram': [],
                    'nachttram': [],
                    'sbahn': [],
                    'ubahn': [],
                    'bus': [],
                    'nachtbus': [],
                    'otherlines': []
                }
            },
         ]

    """
    if lat == 0 or lon == 0:
        return None

    if not (isinstance(lat, float) and isinstance(lon, float)):
        raise TypeError()

    url = nearby_url.format(lat=lat, lon=lon)

    results = _perform_api_request(url)
    return results['locations']


def get_id_for_station(station_name):
    """Returns the station_id for the given station name.

    If more than one station match, the first result is given.
    `None` is returned if no match was found.
    """
    try:
        station = get_stations(station_name)[0]
    except IndexError:
        return None
    return station['id']


def get_locations(query):
    """Returns all matches from the search for the given query string.

    `query` can either be a name of a station or of a street, square, etc.

    Returns a list wich looks somewhat like this::

        [
            {
                'type': 'station',
                'latitude': 48.12046,
                'longitude': 11.61869,
                'id': 'de:09162:1060',
                'place': 'München',
                'name': 'Innsbrucker Ring',
                'hasLiveData': True,
                'hasZoomData': True,
                'products': ['UBAHN'],
                'aliases': 'Muenchen Munchen',
                'link': 'IR',
                'lines': {
                    'tram': [],
                    'nachttram': [],
                    'sbahn': [],
                    'ubahn': [],
                    'bus': [],
                    'nachtbus': [],
                    'otherlines': []
                }
            },
        ]

    """
    try:
        query = "{}{}".format(id_prefix, int(query))  # converts old style station id to new style station id
    except(ValueError):  # happens if it is a station name
        url = query_url_name.format(name=query)
    else:  # happens if it is a station id
        url = query_url_id.format(id=str(query))

    results = _perform_api_request(url)
    return results["locations"]


def get_stations(station):
    """Like :func:`.get_locations`, but filters out all results which
    are not stations.
    """
    results = get_locations(station)
    stations = []
    for result in results:
        if result['type'] == 'station':
            stations.append(result)
    return stations


def get_route(start, dest,
              time=None, arrival_time=False,
              max_walk_time_to_start=None, max_walk_time_to_dest=None,
              change_limit=None,
              ubahn=True,
              bus=True,
              tram=True,
              sbahn=True):
    """Plans a route from start to dest

    Change in 1.3.2: accepts both 'old-style' integer IDs which were used
    by the API before this version and the new string IDs which
    look like `de:09162:6`.

    Parameters
    ----------
    start : int/str/tuple
        The `station_id` of the starting station or a tuple of coordinates
    dest : int/str/tuple
        `station_id` of the destination station or a tuple of coordinates
    time : datetime, optional
    arrival_time : bool, optional
        Specifies if `time` is the starting time (which is default) or
        the desired time of arrival.
    max_walk_time_to_start, max_walk_time_to_dest : int, optional
        Maximum time of walking in minutes required to reach the start/dest.
    changeLimit : int, optional
        Specifies the maximum amount of changes.
    ubahn: bool, optional
        Specifies if the subway(UBahn) should be considered in the route
    bus: bool, optional
        Specifies if the bus should be considered in the route
    tram: bool, optional
        Specifies if the tram should be considered in the route
    sbahn: bool, optional
        Specifies if the SBahn should be considered in the route
    """
    url = routing_url
    options = []


    if isinstance(start, tuple) and len(start) == 2:
        options.append("fromLatitude=" + str(start[0]))
        options.append("fromLongitude=" + str(start[1]))
    elif isinstance(start, int):
        options.append("fromStation=" + _convert_id(start))
    elif _station_sanity_check(start):
        options.append("fromStation=" + start)
    else:
        raise ValueError("A start must be given;\
                          either int station id, 'new style' string ids \
                          or a tuple with latitude and longitude")


    if isinstance(dest, tuple) and len(dest) == 2:
        options.append("toLatitude=" + str(dest[0]))
        options.append("toLongitude=" + str(dest[1]))
    elif isinstance(dest, int):
        options.append("toStation=" + _convert_id(dest))
    elif _station_sanity_check(dest):
        options.append("toStation=" + dest)
    else:
        raise ValueError("A destination must be given;\
                          either int station id or tuple latitude longitude")

    if time:
        if isinstance(time, datetime.datetime):
            time = _convert_time(time)
        options.append("time=" + str(time))
        if arrival_time:
            options.append("arrival=true")
    if max_walk_time_to_start:
        options.append("maxTravelTimeFootwayToStation=" +
                       str(max_walk_time_to_start))
    if max_walk_time_to_dest:
        options.append("maxTravelTimeFootwayToDestination=" +
                       str(max_walk_time_to_dest))

    if change_limit is not None:  # 'if change_limit:' would not work for 0
        if isinstance(change_limit, int):
            options.append("changeLimit=" + str(change_limit))

    if not ubahn:
        options.append("transportTypeUnderground=false")
    if not bus:
        options.append("transportTypeBus=false")
    if not tram:
        options.append("transportTypeTram=false")
    if not sbahn:
        options.append("transportTypeSBahn=false")

    options_url = "&".join(options)
    url = routing_url + options_url
    results = _perform_api_request(url)
    for connection in results["connectionList"]:
        connection["departure_datetime"] = \
            _convert_time(connection["departure"])
        connection["arrival_datetime"] = _convert_time(connection["arrival"])
    return results["connectionList"]


def get_departures(station_id, timeoffset=0):
    """Get the next departures for `station_id`. Optionally, define `timeoffset`
    to not show departures sooner than a number of minutes.

    Change in 1.3.2: accepts both 'old-style' integer IDs which were used
    by the API before this version and the new string IDs which
    look like `de:09162:6`.

    To get the `station_id` associated with a station name,
    use :func:`get_id_for_station`.

    Returns a list like::

        [
            {
                'departureTime': 1571923180000,
                'product': 'UBAHN',
                'label': 'U2',
                'destination': 'Messestadt Ost',
                'live': True,
                'lineBackgroundColor': '#dd3d4d',
                'departureId': 1152101303,
                'sev': False,
                'departureTimeMinutes': 0
            },
        ]

    `departureTimeMinutes`, the time left to the departure in minutes,
    is added to the response from the api for your convenience.
    """
    if isinstance(station_id, int):
        station_id = _convert_id(station_id)
    elif not _station_sanity_check(station_id):
        raise TypeError("Please give the int station_id of the station.\
                         You can find it out by running \
                         get_id_for_station('Station name')")
    url = departure_url.format(id=station_id, offset=timeoffset)
    departures = _perform_api_request(url)['departures']
    for departure in departures:
        # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
        # Here, we convert it to datetime
        time = _convert_time(departure['departureTime'])
        relative_time = time - datetime.datetime.now()
        if 'delay' in departure:
            delay = departure['delay']
        else:
            delay = 0
        departure[u'departureTimeMinutes'] = relative_time // datetime.timedelta(seconds=60) + delay
    return departures


def get_lines(station_id):
    """Get the lines being served for `station_id`.

    Change in 1.3.2: accepts both 'old-style' integer IDs which were used
    by the API before this version and the new string IDs which
    look like `de:09162:6`.
    
    To get the `station_id` associated with a station name,
    use :func:`get_id_for_station`.

    Returns a list like::

        [
            {
                "destination" : "Aying",
                "sev" : false,
                "partialNet" : "ddb",
                "product" : "SBAHN",
                "lineNumber" : "S7",
                "divaId" : "92M07"
            },
        ]

    Note: The api seemingly only returns a single object per 
    line served, meaning that both directions of a line are  
    represented only by a single line in the response.
    """
    if isinstance(station_id, int):
        station_id = _convert_id(station_id)
    elif not _station_sanity_check(station_id):
        raise TypeError("Please give the int station_id of the station.\
                         You can find it out by running \
                         get_id_for_station('Station name')")
    url = departure_url.format(id=station_id, offset=0)
    return _perform_api_request(url)['servingLines']


def get_interruptions():
    url = interruptions_url
    interruptions = _perform_api_request(url)
    return interruptions


class Station:
    """Gives you a proxy to get the next departures for a particular
    station.

    Either give it an exact station name (like "Hauptbahnhof")
    or a station_id.

    Deprecated-ish: This is not really all that useful.
    Just using :func:`get_id_for_station` and :func:`get_departures`
    really is the nicer way in most cases.
    """

    def __init__(self, station):
        matching_stations = get_stations(station)
        if matching_stations == []:
            raise NameError("No matching station found")
        else:
            self.id = matching_stations[0]["id"]
            self.name = matching_stations[0]["name"]
            self.latitude = matching_stations[0]["latitude"]
            self.longitude = matching_stations[0]["longitude"]

    def get_departures(self, timeoffset=0):
        return get_departures(self.id, timeoffset)

    def get_lines(self):
        return get_lines(self.id)

    def __repr__(self):
        return "Station(id=%s, name='%s')" % (self.id, self.name)
