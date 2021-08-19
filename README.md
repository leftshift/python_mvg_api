# python_mvg_api

A library for fetching departures, routes and service interruptions from Munich Transport Authority MVG, using the newer JSON-api on mvg.de

## Get it on pypi:
`pip install mvg-api`


Then, `import mvg_api`.

To get the id for a particular Station, use something like `mvg_api.get_id_for_station("Hauptbahnhof")`.

You can use this id for getting departures with `mvg_api.get_departures(6)` and use it as the start or end of a route.

## Usage policy of the MVG api
From https://www.mvg.de/impressum.html:
```
[...] Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar.[...]
```

In other words: Private, noncomercial, moderate use of the API is tolerated. They don't consider data mining as moderate use.

(Disclaimer: I am not a lawyer, this isn't legal advice)

## Documentation
[Read the Documentation](http://python-mvg-departures.readthedocs.io/en/latest/?)
