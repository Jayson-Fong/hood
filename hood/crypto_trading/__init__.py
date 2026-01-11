import dataclasses
import json
import logging
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
    # noinspection PyUnresolvedReferences
    from _typeshed import DataclassInstance


_T = TypeVar("_T", bound="DataclassInstance")
_U = TypeVar("_U", bound="DataclassInstance")

_logger = logging.getLogger(__package__)


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
        """
        Create HTTP authorization headers by signing the request data with the client's credential.

        Args:
            path: Request path (used in the signature).
            body: Request body as a string (used in the signature).
            method: HTTP method of the request (used in the signature).

        Returns:
            A mapping containing `x-api-key`, `x-signature`, and `x-timestamp` header values.
        """

        timestamp = _util.get_current_timestamp()

        signature = self.credential.sign_message(path, body, timestamp, method)
        _logger.debug("Generated signature %s", signature)
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
        """
        Send a signed HTTP request to the client's API endpoint.

        Args:
            path: The API path or endpoint (may include a base path; query string will be injected from `params`).
            body: JSON-encoded request body; when empty, a body is not sent.
            method: HTTP method enum that provides a `send` implementation for performing the request.
            headers: Additional headers to merge into the generated authorization headers.
            params: Query parameters to inject into the request URL.

        Returns:
            A tuple where the first element is the `requests.Response` if the request succeeded, otherwise `None`;
            the second element is the exception encountered when a request error occurred, otherwise `None`.
        """

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
        """
        Convert a (response, exception) pair into an APIResponse, parsing the HTTP body with the provided schemas.

        Args:
            result: Tuple of an HTTP response or None and Exception or None.
            success_schema: Schema used to parse successful responses (status codes outside 400-599).
            error_schema: Schema used to parse error responses (status codes 400-599).

        Returns:
            An APIResponse containing:
              - error set to the exception if the response is None;
              - response and parsed `data` when a response is present.
        """

        response, exc = result
        if response is None:
            return _structs.APIResponse(error=exc)

        # If the response code indicates an error, attempt parsing using the `error` schema.
        if 400 <= response.status_code < 600:
            _logger.error(
                "Received error response: %d - %s",
                response.status_code,
                response.request.url,
            )

            return _structs.APIResponse(
                response=response,
                data=_parse.parse_response(response, error_schema),
            )

        return _structs.APIResponse(
            response=response,
            data=_parse.parse_response(response, success_schema),
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
        """
        Send a signed HTTP request to the given path and return a parsed APIResponse using the provided schemas.

        Args:
            path: The API path or endpoint (may include a base path; query string will be injected from `params`).
            body: JSON-encoded request body; when empty, a body is not sent.
            method: HTTP method enum that provides a `send` implementation for performing the request.
            headers: Additional headers to merge into the generated authorization headers.
            params: Query parameters to inject into the request URL.
            success_schema: Dataclass or parsing schema to interpret a successful (2xx) response body.
            error_schema: Dataclass or parsing schema to interpret an error (4xx/5xx) response body.

        Returns:
            An APIResponse containing the parsed success data.
        """

        result = self.make_api_request(
            path, body=body, method=method, headers=headers, params=params
        )
        return self.parse_response(result, success_schema, error_schema)


__all__ = ["CryptoTradingClient", "auth"]
