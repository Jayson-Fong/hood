from typing import Protocol, Dict, Optional, TYPE_CHECKING

from . import constants as _constants

if TYPE_CHECKING:
    from . import auth as _auth, structures as _structs


class Client(Protocol):

    credential: "_auth.Credential"
    base_url: str

    def get_authorization_header(
        self,
        path: str,
        body: str,
        method: _constants.RequestMethod,
    ) -> Dict[str, str]: ...

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


__all__ = ["Client"]
