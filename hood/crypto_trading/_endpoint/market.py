from typing import TYPE_CHECKING, Literal, Union

from .._protocols import Client as _Client
from ...schema import market as _schema

if TYPE_CHECKING:
    from .. import structures as _structs


class MarketMixin(_Client):

    def best_bid_ask(
        self,
        *symbols: str,
        **kwargs,
    ) -> "_structs.APIResponse[_schema.BestBidAskResults]":
        return self.make_parsed_api_request(
            "api/v1/crypto/marketdata/best_bid_ask/",
            params={"symbol": list(symbols)},
            success_schema=_schema.BestBidAskResults,
            **kwargs,
        )

    def estimated_price(
        self,
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int],
        **kwargs,
    ) -> "_structs.APIResponse[_schema.MarketEstimateResults]":
        return self.make_parsed_api_request(
            "api/v1/crypto/marketdata/estimated_price/",
            params={
                "symbol": symbol,
                "side": side,
                "quantity": ",".join((str(q) for q in quantity)),
            },
            success_schema=_schema.MarketEstimateResults,
            **kwargs,
        )


__all__ = ["MarketMixin"]
