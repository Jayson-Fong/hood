from typing import TYPE_CHECKING, Literal, Union

from .._protocols import Client as _Client
from ..schema import market as _schema

if TYPE_CHECKING:
    import decimal
    from .. import structures as _structs


class MarketMixin(_Client):

    def best_bid_ask(
        self,
        *symbols: str,
    ) -> "_structs.MaybeAPIResponse[_schema.BestBidAskResults]":
        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/marketdata/best_bid_ask/",
            params={"symbol": list(symbols)},
            success_schema=_schema.BestBidAskResults,
            error_schema=_schema.Errors,
        )

    def estimated_price(
        self,
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int, "decimal.Decimal"],
    ) -> "_structs.MaybeAPIResponse[_schema.MarketEstimateResults]":
        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/marketdata/estimated_price/",
            params={
                "symbol": symbol,
                "side": side,
                "quantity": ",".join((str(q) for q in quantity)),
            },
            success_schema=_schema.MarketEstimateResults,
            error_schema=_schema.Errors,
        )


__all__ = ["MarketMixin"]
