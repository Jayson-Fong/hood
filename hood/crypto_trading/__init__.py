import dataclasses
import json
import urllib.parse
from typing import Dict, Optional, Type, Tuple, TypeVar, Union, TYPE_CHECKING

import requests

# `auth` is purposefully exposed here for convenience.
from . import (
    auth,
    constants as _constants,
    util as _util,
    _endpoint,
    structures as _structs,
    parse as _parse,
)

if TYPE_CHECKING:
    from _typeshed import DataclassInstance  # noqa


_T = TypeVar("_T", bound="DataclassInstance")
_U = TypeVar("_U", bound="DataclassInstance")


@dataclasses.dataclass(slots=True)
class CryptoTradingClient(
    _endpoint.AccountsMixin, _endpoint.MarketMixin, _endpoint.TradingMixin
):

    credential: auth.Credential
    timeout: float = 10.0
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
        *,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
    ) -> Tuple[Optional[requests.Response], Optional[BaseException]]:
        request_target = _util.inject_qs(path, params)
        request_headers = self.get_authorization_header(request_target, body, method)
        if headers:
            request_headers |= headers

        url = urllib.parse.urljoin(self.base_url, request_target)

        try:
            if body:
                return (
                    method.send(
                        url,
                        headers=request_headers,
                        json=json.loads(body),
                        timeout=self.timeout,
                    ),
                    None,
                )

            return (
                method.send(url, headers=request_headers, timeout=self.timeout),
                None,
            )
        except requests.RequestException as err:
            return None, err

    @staticmethod
    def parse_response(
        result: Tuple[Optional[requests.Response], Optional[BaseException]],
        success_schema: Optional[Type[_T]] = None,
        error_schema: Optional[Type[_U]] = None,
    ) -> _structs.APIResponse[Union[_T, _U]]:
        response, exc = result
        if response is None:
            return _structs.APIResponse(error=exc)

        # If the response code indicates an error, attempt parsing using the `error` schema.
        if 400 <= response.status_code < 600:
            return _structs.APIResponse(
                response=response,
                data=_parse.parse_response(response, error_schema),
                error=exc,
            )

        return _structs.APIResponse(
            response=response,
            data=_parse.parse_response(response, success_schema),
            error=exc,
        )

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def make_parsed_api_request(
        self,
        path: str,
        *,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
        success_schema: Optional[Type[_T]] = None,
        error_schema: Optional[Type[_U]] = None,
    ) -> _structs.APIResponse[Union[_T, _U]]:
        result = self.make_api_request(
            path, body=body, method=method, headers=headers, params=params
        )
        return self.parse_response(result, success_schema, error_schema)


__all__ = ["CryptoTradingClient", "auth"]
