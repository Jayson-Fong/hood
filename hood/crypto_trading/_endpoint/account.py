from typing import TYPE_CHECKING

from .._protocols import Client as _Client
from ..schema import account as _schema

if TYPE_CHECKING:
    from .. import structures as _structs


# pylint: disable=too-few-public-methods
class AccountsMixin(_Client):

    def accounts(self) -> "_structs.APIResponse[_schema.TradingAccountDetail]":
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/accounts/",
            success_schema=_schema.TradingAccountDetail,
        )


__all__ = ["AccountsMixin"]
