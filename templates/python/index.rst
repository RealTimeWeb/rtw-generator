.. {{ metadata.name | flat_case }} documentation master file, created by
   sphinx-quickstart on Tue Jul 23 13:06:29 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {{ metadata.name | flat_case }}'s documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2
   
Data Classes
------------

{% for object in objects %}
.. autoclass:: {{ metadata.name | flat_case }}.main.{{ object.name | camel_case_caps }}
    :members:
    :special-members: __init__
{% endfor %}
    
Functions
---------

.. autofunction:: {{ metadata.name | flat_case }}.main.connect

.. autofunction:: {{ metadata.name | flat_case }}.main.disconnect

{% for function in functions %}
.. autofunction:: {{ metadata.name | flat_case }}.main.{{ function.name | snake_case }}
{% endfor %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

