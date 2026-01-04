import dataclasses
import json
import urllib.parse
from typing import Dict, Optional, Type, Tuple

import requests

# `auth` is purposefully exposed here for convenience.
from . import (
    auth,
    constants as _constants,
    util as _util,
    _endpoint,
    structures as _structs,
)

from .. import schema as _schema


@dataclasses.dataclass
class CryptoTradingClient(
    _endpoint.AccountsMixin, _endpoint.MarketMixin, _endpoint.TradingMixin
):

    credential: auth.Credential
    base_url: str = _constants.ROBINHOOD_BASE_URL

    def get_authorization_header(
        self,
        path: str,
        body: str,
        method: _constants.RequestMethod,
    ) -> Dict[str, str]:
        timestamp = _util.get_current_timestamp()
        signature = self.credential.sign_message(path, body, timestamp, method)

        return {
            "x-api-key": self.credential.api_key,
            "x-signature": signature,
            "x-timestamp": str(timestamp),
        }

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def make_api_request(
        self,
        path: str,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
        timeout: float = 10.0,
    ) -> Tuple[Optional[requests.Response], Optional[BaseException]]:
        request_target = _util.inject_qs(path, params)
        request_headers = self.get_authorization_header(request_target, body, method)
        if headers:
            request_headers |= headers

        url = urllib.parse.urljoin(self.base_url, request_target)

        try:
            if body:
                return method.send(
                    url, headers=request_headers, json=json.loads(body), timeout=timeout
                ), None
            else:
                return method.send(url, headers=request_headers, timeout=timeout), None
        except requests.RequestException as err:
            return None, err

    @staticmethod
    def parse_response(
        result: Tuple[Optional[requests.Response], Optional[BaseException]],
        success: Optional[Type] = None,
        error: Optional[Type] = _schema.Errors,
    ) -> _structs.APIResponse:
        response, exc = result
        if response is None:
            return _structs.APIResponse(error=exc)

        # If the response code indicates an error, attempt parsing using the `error` schema.
        if 400 <= response.status_code < 600:
            if not error:
                return _structs.APIResponse(response=response, error=exc)

            # TODO: Parse using schema
            return _structs.APIResponse(error=exc)

        if not success:
            return _structs.APIResponse(response=response)

        # Attempt parsing using the `success` schema.
        # TODO: Parse using schema
        return _structs.APIResponse(response=response)


__all__ = ["CryptoTradingClient", "auth"]
