pywarsaw
========

An unofficial asynchronous API wrapper for `Warsaw Open
Data <https://api.um.warszawa.pl/>`__.

Created mainly for learning purposes.

Features
--------

-  **Asynchronous**: designed to work with asyncio
-  **Extensive**: cover as many endpoints as possible
-  **Approachable**: all polish fields translated to english
-  **Responsible**: minimize the load on the API server

   -  implemented caching

-  **Simple**: easy to use and customize:

   -  object-oriented design
   -  use of data transfer objects
   -  type hinting
   -  convert adequate fields from strings to the more suitable types

-  **Lightweight**: minimal usage of the third-party packages

Installation
------------

::

   pip install pywarsaw

Getting started
---------------

The package goal is to be straightforward to use. For example, you can
obtain a list of objects with information about current air quality in
Warsaw, with caching enabled like this:

.. code:: python

   import asyncio
   import pywarsaw

   async def main():
       client = pywarsaw.Mermaid(api_key="YOUR_API_KEY")
       await client.cache_enable()

       result = await client.get_air_quality()
       
       await client.close()

   asyncio.run(main())

Or with the context manager:

.. code:: python

   async with pywarsaw.Mermaid(api_key="YOUR_API_KEY") as client:
       await client.cache_enable()
       
       result = await client.get_air_quality()

Caching can be disabled with:

.. code:: python

   await client.cache_disable()

Every object from the obtained list an be converted to the simpler
structures:

.. code:: python

   # convert object to the dictionary
   result_dict = result[0].to_dict()

   # convert object to the tuple
   result_tuple = result[0].to_tuple()

   # convert object to the flat dict - useful for creating Pandas dataframes
   result_flat = result[0].to_flat_dict()

   # convert object to the json string
   result_json = result[0].to_json()

Terms of data usage
-------------------

Translated from `here <https://api.um.warszawa.pl/#>`__.

Public data available on the service are official materials and as such
are not protected by copyright law. You may use this data freely but
must comply with the conditions for reusing public information outlined
in the law on the reuse of public sector information of 25th February
2016.

When using public information made available on the Open Data After
Warsaw service, you must: 

- Include information about the source of the data, including the name: Capital City of Warsaw, and the URL of the Open Data After Warsaw service: http://api.um.warszawa.pl (if possible)
- Provide the date of creation and acquisition of public information

Reusing public sector information available on the service is done at
your own risk. The Capital City of Warsaw assumes no responsibility for
any damage resulting from your or other users’ reuse of this
information. Some of the information processed by third parties that you
may reuse may be outdated or contain errors, and the Capital City of
Warsaw reserves the right to this possibility.

Documentation
-------------

The documentation is hosted on
`ReadTheDocs.io <https://pywarsaw.readthedocs.io/en/latest/>`__

Help, questions, and contributing
---------------------------------

All contributors are very welcome. If you have any questions or a bug to
report feel free to open an issue.

External packages
-----------------

Pywarsaw depends on these third-party packages:

-  `attrs <https://www.attrs.org/en/stable/>`__
-  `aiohttp <https://docs.aiohttp.org/en/stable/>`__
-  `aiohttp-client-cache <https://pypi.org/project/aiohttp-client-cache/>`__
-  `aiosqlite <https://github.com/omnilib/aiosqlite>`__

Main class and submodules
-------------------------
From here you can refer to the main class - Yuki and submodules documentation.

.. toctree::
   :maxdepth: 4
   :titlesonly:

   modules

Index
==================

* :ref:`genindex`