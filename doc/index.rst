.. python_mvg_api documentation master file, created by
   sphinx-quickstart on Tue Nov  8 21:17:56 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

python_mvg_api – Munich Public Transport made simple
===========================================================


.. Contents:

.. toctree::
   :maxdepth: 2

Intro
-----
Not too long ago, MVG (aka Münchner Verkehrsgesellschaft) relaunched their `Website <http://mvg.de>`_, which now actually utilizes a JSON api! (I know, crazy, right?) This python module tries to provide easy to use access to most aspects of the mvg api.


It offers:

* The next departures for any station in the MVV

  * This includes S-Bahn and Schienenersatzverkehr

* Listing nearby stations based on geolocation
* Search for Stations and POI
* Routing
* Current warnings about service interruptions


Take a look at example.py, it shows some basic concepts, or at the rest of the docs, where everything should be adequately documented.

Note on the usage policy
------------------------
From https://www.mvg.de/impressum.html:

``[...] Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar.[...]``

In other words: Private, noncomercial, moderate use of the API is tolerated. They don't consider data mining as moderate use.

(Disclaimer: I am not a lawyer, this isn't legal advice)


Module documentation
--------------------

.. automodule:: mvg_api
      :members:

Indices and tables
------------------

* :ref:`genindex`
.. * :ref:`modindex`
* :ref:`search`
