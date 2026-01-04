from typing import Protocol, Dict, Optional, TYPE_CHECKING, Union, TypeVar, Type

from . import constants as _constants

if TYPE_CHECKING:
    from . import auth as _auth, structures as _structs


T = TypeVar("T", bound=Type)
K = TypeVar("K", bound=Type)


class Client(Protocol):

    credential: "_auth.Credential"
    base_url: str

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def make_api_request(
        self,
        path: str,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
        timeout: float = 10.0,
    ) -> "_structs.APIResponse": ...

    def make_parsed_api_request(
        self,
        path: str,
        body: str = "",
        method: _constants.RequestMethod = _constants.RequestMethod.GET,
        headers: Optional[Dict[str, str]] = None,
        params: Optional["_structs.QueryParams"] = None,
        timeout: float = 10.0,
        success_schema: Optional[T] = None,
        error_schema: Optional[K] = None,
    ) -> "_structs.APIResponse[Union[T, K]]": ...


__all__ = ["Client"]
