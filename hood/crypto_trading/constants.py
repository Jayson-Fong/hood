from enum import IntEnum

import requests


ROBINHOOD_BASE_URL = "https://trading.robinhood.com/"

METHODS = (requests.get, requests.post)


class RequestMethod(IntEnum):
    GET = 0
    POST = 1

    def send(self, *args, **kwargs) -> requests.Response:
        """
        Dispatches the enum to the corresponding HTTP function.

        Args:
            *args: Positional arguments forwarded to the selected requests function.
            **kwargs: Keyword arguments forwarded to the selected requests function.

        Returns:
            The response returned by the underlying requests call.
        """

        return METHODS[self.value](*args, **kwargs)

    def __str__(self) -> str:
        """
        Get the enum member's name as a string.

        Returns:
            The enum member's name.
        """

        return self.name


__all__ = ["RequestMethod"]
