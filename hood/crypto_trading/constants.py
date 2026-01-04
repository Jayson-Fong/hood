from enum import IntEnum

import requests


ROBINHOOD_BASE_URL = "https://trading.robinhood.com/"

METHODS = (requests.get, requests.post)


class RequestMethod(IntEnum):
    GET = 0
    POST = 1

    def send(self, *args, **kwargs):
        return METHODS[self.value](*args, **kwargs)

    def __str__(self) -> str:
        return self.name


__all__ = ["RequestMethod"]
