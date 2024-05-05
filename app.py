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

    def ping(self):
        url = f"{self.root_url}/v0/markets?limit=1"
        response = requests.get(url)
        return self.__response_code(response)

    def get_user_info(self, name):
        url = f"{self.root_url}/v0/user/{name}"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        return self.__response_code(response)

    def get_user_info_lite(self, name):
        url = f"{self.root_url}/v0/user/{name}/lite"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        return self.__response_code(response)


load_dotenv()

bot = Bot(getenv("API_KEY"))
print(bot.ping())
print(bot.get_user_info("And"))
print(bot.get_user_info_lite("And"))
