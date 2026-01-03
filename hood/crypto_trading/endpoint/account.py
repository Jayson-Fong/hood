from typing import TYPE_CHECKING, Literal, Protocol, overload

from .. import structures as _structs

if TYPE_CHECKING:
    from .. import CryptoTradingClient


class TradingAccountDetail(Protocol):
    account_number: str
    status: Literal["active", "deactivated", "sell_only"]
    buying_power: str
    buying_power_currency: str


class AccountsMixin:

    @overload
    def accounts(
        self: "CryptoTradingClient", create_namespace: bool = True, **kwargs
    ) -> _structs.APIResponse[TradingAccountDetail]: ...

    def accounts(self: "CryptoTradingClient", **kwargs):
        return self.make_json_api_request("api/v1/crypto/trading/accounts/", **kwargs)
