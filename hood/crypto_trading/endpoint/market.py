from typing import TYPE_CHECKING, Literal, Protocol, overload, Union

from .. import structures as _structs

if TYPE_CHECKING:
    from .. import CryptoTradingClient


class BestBidAskResult(Protocol):
    symbol: str
    price: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    timestamp: str


class MarketMixin:

    @overload
    def best_bid_ask(
        self: "CryptoTradingClient",
        *symbols: str,
        create_namespace: bool = True,
        **kwargs,
    ) -> _structs.ResultsResponse[BestBidAskResult]: ...

    def best_bid_ask(self: "CryptoTradingClient", *symbols: str, **kwargs):
        return self.make_json_api_request(
            "api/v1/crypto/marketdata/best_bid_ask/",
            params={"symbol": list(symbols)},
            **kwargs,
        )

    def estimated_price(
        self: "CryptoTradingClient",
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int],
        **kwargs,
    ):
        return self.make_json_api_request(
            "api/v1/crypto/marketdata/estimated_price/",
            params={
                "symbol": symbol,
                "side": side,
                "quantity": ",".join((str(q) for q in quantity)),
            },
            **kwargs,
        )
