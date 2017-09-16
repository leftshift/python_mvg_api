# python_mvg_api

A library for fetching departures, routes and service interruptions from Munich Transport Authority MVG, using the newer JSON-api on mvg.de

## Get it on pypi:
`pip install mvg-api`


Then, `import mvg_api`.

To get the id for a particular Station, use something like `mvg_api.get_id_for_station("Hauptbahnhof")`.

You can use this id for getting departures with `mvg_api.get_departures(6)` and use it as the start or end of a route.

## Documentation
[Read the Documentation](http://python-mvg-departures.readthedocs.io/en/latest/?)
