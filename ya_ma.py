# -*- coding: utf-8 -*-
""" Yandex maps data requester"""

__version__ = "0.3.7"
__author__ = "Rishat Askarov"
__author_email__ = "Rishatik92@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/rishatik92/ya_ma"

import json
import re

import requests

PARAMS = "params"
AJAX_KEY = "ajax"
LANG_KEY = "lang"
SESSION_KEY = "sessionId"
CSRF_TOKEN_KEY = "csrfToken"
ID_KEY = "id"
LOCALE_KEY = "locale"
MODE_KEY = "mode"
URI_KEY = "uri"
RESOURCE = "https://yandex.ru/maps/api/masstransit/getStopInfo"
DEFAULT_USER_AGENT = "https://pypi.org/project/ya-ma"
CONFIG = {
    "init_url": "https://maps.yandex.ru",
    "uri": RESOURCE,
    "params": {AJAX_KEY: 1, LANG_KEY: "ru", LOCALE_KEY: "ru_RU", MODE_KEY: "prognosis"},
    "headers": {"User-Agent": DEFAULT_USER_AGENT},
}

SCHEMA = [
    AJAX_KEY,
    CSRF_TOKEN_KEY,
    ID_KEY,
    LANG_KEY,
    LOCALE_KEY,
    MODE_KEY,
    SESSION_KEY,
    URI_KEY,
]


class YandexMapsRequester:
    """Implementation of yandex maps api"""

    def __init__(self, user_agent: str = None):
        """
        :type user_agent: set user agent for data requester
        """
        self._config = CONFIG
        if user_agent is not None:
            CONFIG["headers"]["User-Agent"] = user_agent
        self.set_new_session()

    def get_stop_info(self, stop_id):
        """"
        get transport data for stop_id in json
        """
        self._config[PARAMS][ID_KEY] = f"stop__{stop_id}"
        self._config[PARAMS][URI_KEY] = f"ymapsbm1://transit/stop?id=stop__{stop_id}"
        req = requests.get(
            self._config["uri"],
            params=self._config[PARAMS],
            cookies=self._config["cookies"],
            headers=self._config["headers"],
        )
        result = req.content
        try:
            return json.loads(result.decode("utf8"))
        except json.JSONDecodeError as loads_reply_error:
            return {"error": {"exception": loads_reply_error, "response": result}}

    def set_new_session(self):
        """
        Create new http session to Yandex, with valid csrf_token and session_id
        """
        ya_request = requests.get(
            url=self._config["init_url"], headers=self._config["headers"]
        )
        reply = ya_request.content.decode("utf8")
        self._config[PARAMS][CSRF_TOKEN_KEY] = re.search(
            rf'"{CSRF_TOKEN_KEY}":"(\w+.\w+)"', reply
        ).group(1)
        self._config["cookies"] = dict(ya_request.cookies)
        self._config[PARAMS][SESSION_KEY] = re.search(
            rf'"{SESSION_KEY}":"(\d+.\d+)"', reply
        ).group(1)
        params = {}
        self._config[PARAMS][URI_KEY] = None  # init with none
        self._config[PARAMS][ID_KEY] = None

        for key in SCHEMA:
            params[key] = self._config[PARAMS][key]
        self._config[PARAMS] = params


if __name__ == "__main__":
    import sys
    import getopt

    ARGV = sys.argv[1:]
    HELP_STR = """usage: python -m ya_ma -s <stop_id>
    ATTENTION, DON'T FLOOD WITH IT!,
    Because YANDEX can block your freedom access.
    And you will be forced enter capcha every time when you want get data.
    ВНИМАНИЕ - НЕ ПОСЫЛАЙТЕ ЗАПРОСЫ СЛИШКОМ ЧАСТО, иначе 
    Яндекс будет перенаправлять Вас на страницу ввода капчи.
    """
    try:
        if len(ARGV) > 1:
            ARGS = getopt.getopt(ARGV, "s:v")
            ARG, VALUE = ARGS[0][0]
            if ARG == "-s" and VALUE.isdigit():
                CLIENT = YandexMapsRequester()
                print(CLIENT.get_stop_info(VALUE))
                exit(0)
        print(HELP_STR)

    except getopt.GetoptError:
        print(HELP_STR)
        sys.exit(2)
