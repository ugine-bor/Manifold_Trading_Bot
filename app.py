# Manifold markets trading bot using API requests

import requests

from dotenv import load_dotenv
from os import getenv

from datetime import datetime
import ast
import json


class Bot:
    def __init__(self, api_key):
        self._api_key = api_key
        self.root_url = "https://api.manifold.markets"

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
        response = requests.get(url, headers={"Authorization": f"Key {self._api_key}"})
        return self.__response_code(response)

    def get_groups(self, **kwargs):
        url = f"{self.root_url}/v0/groups"

        before_time = kwargs.pop("before", None)
        if before_time:
            before_time = before_time.ljust(23, '0') if ' ' in before_time else before_time + '.000'
            before_time = str(datetime.strptime(before_time, "%Y.%m.%d %H:%M:%S.%f").timestamp()).replace('.', '')

        available_to = kwargs.pop("available_to_id", None)
        response = requests.get(url, params={"beforeTime": before_time, "availableToUserId": available_to})

        return self.__response_code(response)

    def get_group_by_slug(self, slug, **kwargs):
        url = f"{self.root_url}/v0/group/{slug}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_group_by_id(self, id, **kwargs):
        url = f"{self.root_url}/v0/group/by-id/{id}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_markets(self, **kwargs):
        url = f"{self.root_url}/v0/markets"

        limit = kwargs.pop("limit", 500)
        sort = kwargs.pop("sort", "created-time")
        order = kwargs.pop("order", "desc")
        before = kwargs.pop("before", None)
        user_id = kwargs.pop("user_id", None)
        group_id = kwargs.pop("group_id", None)

        response = requests.get(url, params={"limit": limit, "sort": sort, "order": order, "before": before,
                                             "userId": user_id, "groupId": group_id})
        return self.__response_code(response)

    def get_market_by_id(self, id, **kwargs):
        url = f"{self.root_url}/v0/market/{id}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_market_by_slug(self, slug, **kwargs):
        url = f"{self.root_url}/v0/slug/{slug}"
        response = requests.get(url)
        return self.__response_code(response)

    def get_market_positions(self, id, **kwargs):
        url = f"{self.root_url}/v0/market/{id}/positions"

        order = kwargs.pop("order", "profit")
        top = kwargs.pop("top", None)
        bottom = kwargs.pop("bottom", None)
        user_id = kwargs.pop("user_id", None)

        response = requests.get(url, params={"order": order, "top": top, "bottom": bottom, "userId": user_id})
        return self.__response_code(response)

    def get_markets_by_filter(self, **kwargs):
        url = f"{self.root_url}/v0/search-markets"

        term = kwargs.pop("term", None)
        sort = kwargs.pop("sort", "score")
        fltr = kwargs.pop("filter", "all")
        contract_type = kwargs.pop("contract_type", "ALL")
        topic_slug = kwargs.pop("topic_slug", None)
        creator_id = kwargs.pop("creator_id", None)
        limit = kwargs.pop("limit", 100)
        offset = kwargs.pop("offset", None)

        response = requests.get(url, params={"term": term, "sort": sort, "filter": fltr, "contractType": contract_type,
                                             "topicSlug": topic_slug, "creatorId": creator_id, "limit": limit,
                                             "offset": offset})
        return self.__response_code(response)

    def get_users(self, **kwargs):
        url = f"{self.root_url}/v0/users"

        limit = kwargs.pop("limit", 500)
        before = kwargs.pop("before", None)

        response = requests.get(url, params={"limit": limit, "before": before})
        return self.__response_code(response)

    def get_comments(self, **kwargs):
        url = f"{self.root_url}/v0/comments"

        contract_id = kwargs.pop("contract_id", None)
        contract_slug = kwargs.pop("contract_slug", None)
        limit = kwargs.pop("limit", 5000)
        page = kwargs.pop("page", None)
        user_id = kwargs.pop("user_id", None)

        response = requests.get(url, params={"contractId": contract_id, "contractSlug": contract_slug, "limit": limit,
                                             "page": page, "userId": user_id})
        return self.__response_code(response)

    def get_bets(self, **kwargs):
        url = f"{self.root_url}/v0/bets"

        user_id = kwargs.pop("user_id", None)
        user_name = kwargs.pop("user_name", None)
        contract_id = kwargs.pop("contract_id", None)
        contract_slug = kwargs.pop("contract_slug", None)
        limit = kwargs.pop("limit", 1000)
        before = kwargs.pop("before", None)
        after = kwargs.pop("after", None)
        kinds = kwargs.pop("kinds", None)
        order = kwargs.pop("order", "desc")

        response = requests.get(url, params={"userId": user_id, "username": user_name, "contractId": contract_id,
                                             "contractSlug": contract_slug, "limit": limit, "before": before,
                                             "after": after, "kinds": kinds, "order": order})
        return self.__response_code(response)

    def get_managrams(self, **kwargs):
        url = f"{self.root_url}/v0/managrams"

        to_id = kwargs.pop("to_id", None)
        from_id = kwargs.pop("from_id", None)
        limit = kwargs.pop("limit", 100)
        before = kwargs.pop("before", None)
        after = kwargs.pop("after", None)

        response = requests.get(url, params={"toId": to_id, "fromId": from_id, "limit": limit, "before": before,
                                             "after": after})
        return self.__response_code(response)

    @staticmethod
    def __print(method):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)

            to_print = kwargs.pop("pt", False)
            if to_print:
                print(
                    f"\nMethod: {method.__name__} {'(lite)' if kwargs.pop('lite', False) else ''}\nResult: {result}\n")
            return result

        return wrapper

    ping = __print(ping)
    get_user_info = __print(get_user_info)
    get_user_by_id = __print(get_user_by_id)
    get_me = __print(get_me)
    get_groups = __print(get_groups)
    get_group_by_slug = __print(get_group_by_slug)
    get_group_by_id = __print(get_group_by_id)
    get_markets = __print(get_markets)
    get_market_by_id = __print(get_market_by_id)
    get_market_by_slug = __print(get_market_by_slug)
    get_market_positions = __print(get_market_positions)
    get_markets_by_filter = __print(get_markets_by_filter)
    get_users = __print(get_users)
    get_comments = __print(get_comments)
    get_bets = __print(get_bets)
    get_managrams = __print(get_managrams)


def __main__():
    load_dotenv()

    def print_all(lst):
        if isinstance(lst, list):
            for item in lst:
                print(item)
                pass
        else:
            print(lst)

    # pt = print to console

    bot = Bot(getenv("API_KEY"))
    bot.ping(pt=True)

    # bot.get_user_info("And", pt=True)
    # bot.get_user_info("And", lite=True, pt=True)

    # bot.get_user_by_id("hKURbhPsW2VpezOdAAisTTCIBLn2", pt=True)
    # bot.get_user_by_id("hKURbhPsW2VpezOdAAisTTCIBLn2", lite=True, pt=True)

    # bot.get_me(pt=True)

    # groups = bot.get_groups(before='2023.01.04 22:11:05.123000', available_to_id="hKURbhPsW2VpezOdAAisTTCIBLn2")
    # print_all(groups)

    # bot.get_grpoup_by_slug("astroworld", pt=True)

    # bot.get_group_by_id("72sPPf5PTwnQQWGdZ5cR", pt=True)

    # before shows all lower than choosen
    # markets = bot.get_markets(limit=10, sort='created-time', order='desc', before='YjSqIbphVnHDJxcplwRt', user_id="n3zzATIKccTzFxyifz7vSGNKjHD3")
    # print_all(markets)

    # bot.get_market_by_id("YjSqIbphVnHDJxcplwRt", pt=True)

    market = json.dumps(ast.literal_eval(str(bot.get_market_by_slug("will-gpt-be-said-by-anyone-in-a-pre"))))
    marketid = json.loads(market)['id']

    # positions = bot.get_market_positions(marketid, order='profit', top=10, bottom=10, pt=True)
    # print_all(positions)

    # markets_searched = bot.get_markets_by_filter(term="GPT", sort="newest", filter="closing-this-month", contract_type="BINARY", limit=10, offset=2)
    # print_all(markets_searched)

    # users = bot.get_users(limit=30, before='hKURbhPsW2VpezOdAAisTTCIBLn2')
    # print_all(users)

    # comments = bot.get_comments(contract_id=marketid, limit=10)
    # print_all(comments)

    bets = bot.get_bets(contract_id=marketid, limit=10)
    print_all(bets)

    # managrams = bot.get_managrams(to_id="IPTOzEqrpkWmEzh6hwvAyY9PqFb2")
    # print_all(managrams)


if __name__ == "__main__":
    __main__()
