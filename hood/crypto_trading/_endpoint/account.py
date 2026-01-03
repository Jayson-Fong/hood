from typing import TYPE_CHECKING, overload, Union, Literal


from .._protocols import Client as _Client

if TYPE_CHECKING:
    from .. import structures as _structs
    from ..schema import TradingAccountDetailProtocol as _AccountsP
    from ..schema import TradingAccountDetailDict as _AccountsD


# pylint: disable=too-few-public-methods
class AccountsMixin(_Client):

    @overload
    def accounts(
        self, create_namespace: Literal[False] = False, **kwargs
    ) -> "_structs.APIResponse[_AccountsD]": ...

    @overload
    def accounts(
        self, create_namespace: Literal[True], **kwargs
    ) -> "_structs.APIResponse[_AccountsP]": ...

    def accounts(
        self, create_namespace: bool = False, **kwargs
    ) -> "_structs.APIResponse[Union[_AccountsP, _AccountsD]]":
        return self.make_json_api_request(
            "api/v1/crypto/trading/accounts/",
            create_namespace=create_namespace,
            **kwargs,
        )


__all__ = ["AccountsMixin"]
