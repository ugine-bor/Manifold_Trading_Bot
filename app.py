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
        is_lite = kwargs.get("lite", False)
        if is_lite:
            url = f"{self.root_url}/v0/user/{name}/lite"
        else:
            url = f"{self.root_url}/v0/user/{name}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_user_by_id(self, id, **kwargs):
        is_lite = kwargs.get("lite", False)
        if is_lite:
            url = f"{self.root_url}/v0/user/by-id/{id}/lite"
        else:
            url = f"{self.root_url}/v0/user/by-id/{id}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_me(self, **kwargs):
        url = f"{self.root_url}/v0/me"
        response = requests.get(url, headers={"Authorization": f"Key {self.api_key}"})
        return self.__response_code(response)

    @staticmethod
    def __print(method):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)

            to_print = kwargs.pop("pt", False)
            if to_print:
                print(f"\nMethod: {method.__name__} {'(lite)' if kwargs.pop('lite', False) else ''}\nResult: {result}\n")
            return result

        return wrapper

    ping = __print(ping)
    get_user_info = __print(get_user_info)
    get_user_by_id = __print(get_user_by_id)
    get_me = __print(get_me)


load_dotenv()

# pt = print to console

bot = Bot(getenv("API_KEY"))
bot.ping(pt=True)

bot.get_user_info("And", pt=True)
bot.get_user_info("And", lite=True, pt=True)

bot.get_user_by_id("hKURbhPsW2VpezOdAAisTTCIBLn2", pt=True)
bot.get_user_by_id("hKURbhPsW2VpezOdAAisTTCIBLn2", lite=True, pt=True)

bot.get_me(pt=True)
