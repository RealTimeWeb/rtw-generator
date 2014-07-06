.. weatherservice documentation master file, created by
   sphinx-quickstart on Tue Jul 23 13:06:29 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to weatherservice's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2
   
Data Classes
------------


.. autoclass:: weatherservice.main.Report
    :members:
    :special-members: __init__

.. autoclass:: weatherservice.main.Weather
    :members:
    :special-members: __init__

.. autoclass:: weatherservice.main.Location
    :members:
    :special-members: __init__

.. autoclass:: weatherservice.main.Forecast
    :members:
    :special-members: __init__

    
Functions
---------

.. autofunction:: weatherservice.main.connect

.. autofunction:: weatherservice.main.disconnect


.. autofunction:: weatherservice.main.get_report


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
