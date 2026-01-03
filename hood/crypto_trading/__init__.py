import dataclasses
import json
import urllib.parse
from typing import Dict, Optional

import requests

from . import (
    auth,
    constants as _constants,
    util as _util,
    endpoint as _endpoint,
    structures as _structures,
)


@dataclasses.dataclass
class CryptoTradingClient(_endpoint.AccountsMixin, _endpoint.MarketMixin):

    credential: auth.Credential
    base_url: str = "https://trading.robinhood.com/"

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

    def make_api_request(
        self,
        path: str,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        raise_for_status: bool = True,
        params: Optional[_structures.QueryParams] = None,
        **kwargs,
    ) -> _structures.APIResponse[requests.Response]:
        request_target = _util.inject_qs(path, params)
        request_headers = self.get_authorization_header(request_target, body, method)
        if headers:
            request_headers |= headers

        url = urllib.parse.urljoin(self.base_url, request_target)

        try:
            if body:
                response = method.send(
                    url, headers=request_headers, json=json.loads(body), **kwargs
                )
            else:
                response = method.send(url, headers=request_headers, **kwargs)

            if raise_for_status:
                response.raise_for_status()
        except requests.RequestException as err:
            return None, err

        return response, None

    # TODO: Improve return type
    def make_json_api_request(
        self,
        path: str,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        raise_for_status: bool = True,
        create_namespace: bool = False,
        **kwargs,
    ) -> _structures.APIResponse:
        response, err = self.make_api_request(
            path, body, method, headers, raise_for_status, **kwargs
        )

        if response is None:
            return None, err

        json_response = response.json()
        if create_namespace:
            return _util.dict_to_namespace(json_response), err

        return json_response, err


__all__ = ["CryptoTradingClient"]
