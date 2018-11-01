# python_mvg_api

A library for fetching departures, routes and service interruptions from Munich Transport Authority MVG, using the newer JSON-api on mvg.de

## Get it on pypi:
`pip install mvg-api`


Then, `import mvg_api`.

To get the id for a particular Station, use something like `mvg_api.get_id_for_station("Hauptbahnhof")`.

You can use this id for getting departures with `mvg_api.get_departures(6)` and use it as the start or end of a route.

## Documentation
[Read the Documentation](http://python-mvg-departures.readthedocs.io/en/latest/?)

# Example Application: console program to request the departure time

## Getting started

Add the following line to your `.zshrc`

`alias mvg="python3.5 $HOME/path/to/directory/python_mvg_api/get_info.py"`

Probably not the cleanest way to do it, but it's the only way I know at the moment :)

Please feel free to correct me anywhere if you have a better idea!

## Run
`mvg Studentenstadt` will look up all the departures from the station "Studentenstadt"

`mvg` will run the last station you have looked up

## Demo
![screenshot](demo.png)
