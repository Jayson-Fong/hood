from typing import Protocol, Dict, Optional, TYPE_CHECKING, Union, TypeVar, Type, Tuple

from . import constants as _constants

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from _typeshed import DataclassInstance
    import requests
    from . import auth as _auth, structures as _structs


_T = TypeVar("_T", bound="DataclassInstance")
_U = TypeVar("_U", bound="DataclassInstance")


class Client(Protocol):

    credential: "_auth.Credential"
    timeout: float
    base_url: str

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def make_api_request(
        self,
        path: str,
        *,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
    ) -> Tuple[Optional["requests.Response"], Optional[BaseException]]:
        """
        Send a signed HTTP request to the client's API endpoint.

        Args:
            path: The API path or endpoint.
            body: JSON-encoded request body; when empty, a body is not sent.
            method: HTTP method.
            headers: Additional headers to merge into the generated authorization headers.
            params: Query parameters to inject into the request URL.

        Returns:
            A tuple where the first element is the `requests.Response` if the
            request succeeded, otherwise `None`; the second element is the
            exception encountered when a request error occurred, otherwise `None`.
        """

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
    ) -> "_structs.APIResponse[Union[_T, _U]]":
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


__all__ = ["Client"]
