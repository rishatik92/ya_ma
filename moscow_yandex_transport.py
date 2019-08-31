import re
from json import loads

import requests

__version__      = "0.2.0"
__author__       = "Rishat Askarov"
__author_email__ = "Rishatik92@gmail.com"
__license__      = "MIT"
__url__          = 'https://github.com/rishatik92/moscow_yandex_transport'

""" Yandex maps data requester"""

RESOURCE = 'https://yandex.ru/maps/api/masstransit/getStopInfo'
CONFIG = {
    'init_url': 'https://maps.yandex.ru',
    'uri': RESOURCE,
    'params': {'ajax': 1, 'lang': 'en', 'locale': 'en_EN', 'mode': 'prognosis'},
    'headers': {'User-Agent': "Chrome"}}
SESSION_KEY = "sessionId"
CSRF_TOKEN_KEY = "csrfToken"


class YandexMapsRequester(object):
    def __init__(self, user_agent: str = None):
        """

        :type user_agent: set user agent for data requester
        """
        self._config = CONFIG
        if user_agent is not None:
            CONFIG['headers']['User-Agent'] = user_agent
        self.set_new_session()

    def get_stop_info(self, stop_id):
        """"
        get transport data for stop_id in json
        """
        self._config["params"]["id"] = f"stop__{stop_id}"
        req = requests.get(self._config["uri"], params=self._config["params"], cookies=self._config["cookies"],
                           headers=self._config["headers"])
        return loads(req.content.decode('utf8'))

    def set_new_session(self):
        """
        Create new http session to Yandex, with valid csrf_token and session_id
        """
        ya_request = requests.get(url=self._config["init_url"], headers=self._config["headers"])
        reply = ya_request.content.decode('utf8')
        self._config["params"][CSRF_TOKEN_KEY] = re.search(f'"{CSRF_TOKEN_KEY}":"(\w+.\w+)"', reply).group(1)
        self._config["cookies"] = dict(ya_request.cookies)
        self._config["params"][SESSION_KEY] = re.search(f'"{SESSION_KEY}":"(\d+.\d+)"', reply).group(1)


if __name__ == '__main__':
    client = YandexMapsRequester()
    print(client.get_stop_info(9639579))
