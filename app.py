# Manifold markets trading bot using API requests

import requests

from dotenv import load_dotenv
from os import getenv


class Bot:
    def __init__(self, api_key, root_url="https://api.manifold.markets"):
        self.api_key = api_key
        self.root_url = root_url

    @staticmethod
    def __response_code(res):
        code = res.status_code
        if code == 200:
            return res.json()
        elif code == 400:
            return f"Bad Request - {res}"
        elif code == 401:
            return f"Unauthorized - {res}"
        elif code == 404:
            return f"Not Found - {res}"
        elif code == 500:
            return f"Internal Server Error - {res}"
        else:
            return f"Unknown Error - {res}"

    def ping(self, **kwargs):
        url = f"{self.root_url}/v0/markets?limit=1"
        response = requests.get(url)
        return self.__response_code(response)

    def get_user_info(self, name, **kwargs):
        url = f"{self.root_url}/v0/user/{name}"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        return self.__response_code(response)

    def get_user_info_lite(self, name, **kwargs):
        url = f"{self.root_url}/v0/user/{name}/lite"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        return self.__response_code(response)

    def get_user_by_id(self, id, **kwargs):
        url = f"{self.root_url}/v0/user/by-id/{id}"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        return self.__response_code(response)

    @staticmethod
    def __print(method):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)

            to_print = kwargs.pop("pt", False)
            if to_print:
                print(f"\nMethod: {method.__name__}\nResult: {result}\n")
            return result

        return wrapper

    ping = __print(ping)
    get_user_info = __print(get_user_info)
    get_user_info_lite = __print(get_user_info_lite)
    get_user_by_id = __print(get_user_by_id)


load_dotenv()

bot = Bot(getenv("API_KEY"))
bot.ping(pt=True)
bot.get_user_info("And")
bot.get_user_info_lite("And", pt=True)
