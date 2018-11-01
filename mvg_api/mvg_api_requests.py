#!/usr/bin/env python
""" Interface to the MVG API. """

import requests
import json
import datetime
from time import mktime

API_KEY = "5af1beca494712ed38d313714d4caff6"
BASE_URL = "https://www.mvg.de/"
FAHRINFO_API_PATH = "fahrinfo/api/"
QUERY_URL_WITH_NAME = BASE_URL + FAHRINFO_API_PATH + "location/queryWeb?q={name}" #for station names
QUERY_URL_WITH_ID = BASE_URL + FAHRINFO_API_PATH + "location/query?q={id}" #for station ids
DEPARTURE_URL = BASE_URL + FAHRINFO_API_PATH + "departure/{id}?footway=0"
NEARBY_URL = BASE_URL + FAHRINFO_API_PATH + "location/nearby?latitude={lat}&longitude={lon}"
ROUTING_URL = BASE_URL + FAHRINFO_API_PATH + "routing/?"
INTERRUPTIONS_URL = BASE_URL + ".rest/betriebsaenderungen/api/interruptions"


def _perform_api_request(url):
    """ Request the given URL and return a JSON with the response. """
    response = requests.get(url, headers={'X-MVG-Authorization-Key': API_KEY})
    return response.json()


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
        try:
            timestamp = time / 1000
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception as e:
            raise


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
                'lines':
                    {
                    'nachtbus': [],
                    'ubahn': ['2', '5', '7'],
                    'tram': [],
                    'sbahn': [],
                    'otherlines': [],
                    'nachttram': [],
                    'bus': []
                    },
                'hasLiveData': True,
                'place': 'München',
                'products': ['BUS', 'TRAM', 'UBAHN', 'SBAHN'],
                'id': 1060,
                'type': 'nearbystation',
                'name': 'Innsbrucker Ring',
                'hasZoomData': True,
                'distance': 59,
                'longitude': 11.619138,
                'latitude': 48.120408
             },
         ]

    """
    if lat == 0 or lon == 0:
        return None

    if not (isinstance(lat, float) and isinstance(lon, float)):
        raise TypeError()

    url = NEARBY_URL.format(lat=lat, lon=lon)

    results = _perform_api_request(url)
    return results['locations']


def get_id_for_station(station_name):
    """Returns the station_id for the given station name.

    If more than one station match, the first result is given.
    `None` is returned if no match was found.
    """

    stations = get_stations(station_name)

    # No station found
    if not stations:
        return None
    # At least one station found: Return first
    else:
        return stations[0]['id']


def get_locations(query):
    """Returns all matches from the search for the given query string.

    `query` can either be a name of a station or of a street, square, etc.

    Returns a list wich looks somewhat like this::

        [
            {
                'lines':
                    {
                    'nachtbus': [],
                    'ubahn': ['2', '5', '7'],
                    'tram': [],
                    'sbahn': [],
                    'otherlines': [],
                    'nachttram': [],
                    'bus': []
                    },
                'hasLiveData': True,
                'place': 'München',
                'products': ['u'],
                'id': 1060,
                'type': 'nearbystation',
                'name': 'Innsbrucker Ring',
                'hasZoomData': True,
                'distance': 59,
                'longitude': 11.619138,
                'latitude': 48.120408
            },
        ]

    """
    try:
        query = int(query)  # converts station ids to int if thay aren't already
    except(ValueError):  # happens if it is a station name
        url = QUERY_URL_WITH_NAME.format(name=query)
    else:  # happens if it is a station id
        url = QUERY_URL_WITH_ID.format(id=str(query))

    results = _perform_api_request(url)
    return results["locations"]


def get_stations(station):
    """Like :func:`.get_locations`, but filters out all results which
    are not stations.
    """
    results = get_locations(station)
    stations = [result for result in results if result['type'] == 'station']
    return stations


def get_route(start, dest,
              time=None, time_is_arrival_time=False,
              max_walk_time_to_start=None, max_walk_time_to_dest=None):
    """Plans a route from start to dest

    Parameters
    ----------
    start : int/tuple
        The `station_id` of the starting station or a tuple of coordinates
    dest : int/tuple
        `station_id` of the destination station or a tuple of coordinates
    time : datetime, optional
    time_is_arrival_time : bool, optional
        Specifies if `time` is the starting time (which is default) or
        the desired time of arrival.
    max_walk_time_to_start, max_walk_time_to_dest : int, optional
        Maximum time of walking in minutes required to reach the start/dest.
    """
    options = []

    if isinstance(start, int):
        options.append("fromStation=" + str(start))
    elif isinstance(start, tuple) and len(start) == 2:
        options.append("fromLatitude=" + str(start[0]))
        options.append("fromLongitude=" + str(start[1]))
    else:
        raise ValueError("A start must be given;\
                          either int station id or tuple latitude longitude")

    if isinstance(dest, int):
        options.append("toStation=" + str(dest))
    elif isinstance(dest, tuple) and len(dest) == 2:
        options.append("toLatitude=" + str(dest[0]))
        options.append("toLongitude=" + str(dest[1]))
    else:
        raise ValueError("A destination must be given;\
                          either int station id or tuple latitude longitude")

    if time:
        if isinstance(time, datetime.datetime):
            time = _convert_time(time)
        options.append("time=" + str(time))
        if time_is_arrival_time:
            options.append("arrival=true")
    if max_walk_time_to_start:
        options.append("maxTravelTimeFootwayToStation=" +
                       str(max_walk_time_to_start))
    if max_walk_time_to_dest:
        options.append("maxTravelTimeFootwayToDestination=" +
                       str(max_walk_time_to_dest))

    options_url = "&".join(options)
    url = ROUTING_URL + options_url
    results = _perform_api_request(url)
    for connection in results["connectionList"]:
        connection["departure_datetime"] = \
            _convert_time(connection["departure"])
        connection["arrival_datetime"] = _convert_time(connection["arrival"])
    return results["connectionList"]


def get_departures_by_name(station_name):
    """ Get the departures for a station, specified by its name. """

    station_id = get_id_for_station(station_name)

    if station_id is None:
        raise TypeError("invalid station name")

    return get_departures(station_id)


def get_departures(station_id):
    """Get the next departures for `station_id`.

    To get the `station_id` associated with a station name,
    use :func:`get_id_for_station`.

    Returns a list like::

        [
            {
                'departureTimeMinutes': 0,
                'destination': 'Laimer Platz',
                'sev': False,
                'departureId': 1188266868,
                'live': True,
                'departureTime': 1478644495000,
                'lineBackgroundColor': '#b78730',
                'label': '5',
                'product': 'u'
            },
        ]

    `departureTimeMinutes`, the time left to the departure in minutes,
    is added to the response from the api for your convenience.
    """
    if not isinstance(station_id, int):
        raise TypeError("Please give the int station_id of the station.\
                         You can find it out by running \
                         get_id_for_station('Station name')")

    url = DEPARTURE_URL.format(id=str(station_id))
    departures = _perform_api_request(url)['departures']

    for departure in departures:
        # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
        # Here, we convert it to datetime
        time = _convert_time(departure['departureTime'])
        relative_time = time - datetime.datetime.now()
        departure[u'departureTimeMinutes'] = relative_time.seconds // 60

    return departures


def get_interruptions():
    interruptions = _perform_api_request(INTERRUPTIONS_URL)
    return interruptions
