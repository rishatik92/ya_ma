``moscow_yandex_transport`` is a client library for the YANDEX TRANPORT API
This client can request data for bus stops and present it on python dictionary


Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``moscow_yandex_transport`` and its dependencies::

    pip install moscow_yandex_transport


Example
=======

::

    >>> from moscow_yandex_transport import YandexMapsRequester
    >>> client = YandexMapsRequester()
    >>> print(client.get_stop_info(9639579))

