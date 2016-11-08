.. python_mvg_departures documentation master file, created by
   sphinx-quickstart on Tue Nov  8 21:17:56 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

python_mvg_departures – Munich Public Transport made simple
===========================================================


.. Contents:

.. toctree::
   :maxdepth: 2

Intro
-----
Not too long ago, MVG (aka Münchner Verkehrsgesellschaft) relaunched their `Website <http://mvg.de>`_, which now actually utilizes a JSON api! (I know, crazy, right?) This python module tries to provide super easy, gluten free [1]_ access to most aspects of the mvg api.


It offers:

* The next departures for any station in the MVV (duh)

  * This includes S-Bahn and Schienenersatzverkehr

* Listing nearby stations based on geolocation
* Routing from station to station

  * Routing from anywhere to anywhere (coming soon!)

Take a look at example.py, it shows some basic concepts, or at the rest of the docs, where every aspect is hopefully adequately documented.

.. [1] mvg.de uses stuff like an api key (although *they only give it to themselves*) and Unix time in milliseconds (although the last four digits are always 0). Whith this module, you won't have to worry about all that.

Module documentation
--------------------

.. automodule:: mvg
      :members:

Indices and tables
------------------

* :ref:`genindex`
.. * :ref:`modindex`
* :ref:`search`
