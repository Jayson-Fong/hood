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
        """
        Retrieve the best "bid" and "ask" quotes for one or more symbols.

        Args:
            *symbols: One or more market symbol strings to query.

        Returns:
            MaybeAPIResponse[_schema.BestBidAskResults]: Parsed best-bid and best-ask data for the requested symbols.
        """

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
        """
        Request market estimated price(s) for a symbol and side.

        Args:
            symbol: The market symbol to estimate (e.g., "BTC-USD"). Only USD symbols are accepted.
            side: Which side to estimate prices for.
            *quantity: One or more quantity values.

        Returns:
            Parsed market estimate results on success or parsed error information on failure.
        """

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
