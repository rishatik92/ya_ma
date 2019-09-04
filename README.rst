``ya_ma`` is unofficial client library for the YANDEX MAPS API
This client can request data for bus stops and present it on python dictionary


Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``ya_ma`` and its dependencies::

    pip install ya_ma


Example
=======

::

    >>> from ya_ma import YandexMapsRequester
        >>> client = YandexMapsRequester()
        >>> print(client.get_stop_info(9639579))
    >>> client = YandexMapsRequester()
    >>> print(client.get_stop_info(9639579))

Or you can use it in your shell:
::

    python -m ya_ma -s 9966346

