from typing import Protocol, Dict, Optional, TYPE_CHECKING, Union, TypeVar, Type, Tuple

from . import constants as _constants

if TYPE_CHECKING:
    from _typeshed import DataclassInstance  # noqa
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
    ) -> Tuple[Optional["requests.Response"], Optional[BaseException]]: ...

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
    ) -> "_structs.APIResponse[Union[_T, _U]]": ...


__all__ = ["Client"]
