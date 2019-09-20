
""" Yandex maps data requester"""
__version__ = "0.3.6"
__author__ = "Rishat Askarov"
__author_email__ = "Rishatik92@gmail.com"
__license__ = "MIT"
__url__ = 'https://github.com/rishatik92/ya_ma'

import requests
import re
from json import loads

PARAMS = 'params'
AJAX_KEY = 'ajax'
LANG_KEY = 'lang'
SESSION_KEY = "sessionId"
CSRF_TOKEN_KEY = "csrfToken"
ID_KEY = 'id'
LOCALE_KEY = 'locale'
MODE_KEY= 'mode'
URI_KEY = "uri"
RESOURCE = 'https://yandex.ru/maps/api/masstransit/getStopInfo'
DEFAULT_USER_AGENT = "https://pypi.org/project/ya-ma"
CONFIG = {
    'init_url': 'https://maps.yandex.ru',
    'uri': RESOURCE,
    'params': {AJAX_KEY: 1, LANG_KEY: 'ru', LOCALE_KEY: 'ru_RU', MODE_KEY: 'prognosis'},
    'headers': {'User-Agent': DEFAULT_USER_AGENT}}

SCHEMA = [AJAX_KEY, CSRF_TOKEN_KEY, ID_KEY, LANG_KEY, LOCALE_KEY, MODE_KEY, SESSION_KEY, URI_KEY]

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
        self._config[PARAMS][ID_KEY] = f"stop__{stop_id}"
        self._config[PARAMS][URI_KEY] = f"ymapsbm1://transit/stop?id=stop__{stop_id}"
        req = requests.get(self._config["uri"], params=self._config[PARAMS], cookies=self._config["cookies"],
                           headers=self._config["headers"])
        result = req.content
        try:
            return loads(result.decode('utf8'))
        except Exception as e:
            return {"error": {"exception": e, "response": result}}

    def set_new_session(self):
        """
        Create new http session to Yandex, with valid csrf_token and session_id
        """
        ya_request = requests.get(url=self._config["init_url"], headers=self._config["headers"])
        reply = ya_request.content.decode('utf8')
        self._config[PARAMS][CSRF_TOKEN_KEY] = re.search(f'"{CSRF_TOKEN_KEY}":"(\w+.\w+)"', reply).group(1)
        self._config["cookies"] = dict(ya_request.cookies)
        self._config[PARAMS][SESSION_KEY] = re.search(f'"{SESSION_KEY}":"(\d+.\d+)"', reply).group(1)
        params = {}
        self._config[PARAMS][URI_KEY] = None # init with none
        self._config[PARAMS][ID_KEY] = None

        for key in SCHEMA:
            params[key] = self._config[PARAMS][key]
        self._config[PARAMS] = params

if __name__ == '__main__':
    import sys
    import getopt

    argv = sys.argv[1:]
    help_str = """usage: python -m ya_ma -s <stop_id>
    
    
    ATTENTION, DON'T FLOOD WITH IT!,
    Because YANDEX can block your freedom access. And you will be forced enter capcha every time when you want get data.
    ВНИМАНИЕ - НЕ ПОСЫЛАЙТЕ ЗАПРОСЫ СЛИШКОМ ЧАСТО, иначе Яндекс будет перенаправлять Вас на страницу ввода капчи.
    """
    try:
        if len(argv) > 1:
            args = getopt.getopt(argv, 's:v')
            arg, value = args[0][0]
            if arg == '-s' and value.isdigit():
                client = YandexMapsRequester()
                print(client.get_stop_info(value))
                exit(0)
        print(help_str)

    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
