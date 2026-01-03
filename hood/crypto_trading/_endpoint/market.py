from typing import TYPE_CHECKING, Literal, overload, Union

from .._protocols import Client as _Client

if TYPE_CHECKING:
    from .. import structures as _structs
    from ..schema import BestBidAskProtocol as _BidAskP
    from ..schema import BestBidAskDict as _BidAskD
    from ..schema import MarketEstimateProtocol as _EstimateP
    from ..schema import MarketEstimateDict as _EstimateD


class MarketMixin(_Client):

    @overload
    def best_bid_ask(
        self,
        *symbols: str,
        create_namespace: Literal[False] = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponseDict[_BidAskD]": ...

    @overload
    def best_bid_ask(
        self,
        *symbols: str,
        create_namespace: Literal[True],
        **kwargs,
    ) -> "_structs.MaybeAPIResponseProtocol[_BidAskP]": ...

    def best_bid_ask(
        self,
        *symbols: str,
        create_namespace: bool = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponse[Union[_BidAskP, _BidAskD]]":
        return self.make_json_api_request(
            "api/v1/crypto/marketdata/best_bid_ask/",
            params={"symbol": list(symbols)},
            create_namespace=create_namespace,
            **kwargs,
        )

    @overload
    def estimated_price(
        self,
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int],
        create_namespace: Literal[False] = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponseDict[_EstimateD]": ...

    @overload
    def estimated_price(
        self,
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int],
        create_namespace: Literal[True],
        **kwargs,
    ) -> "_structs.MaybeAPIResponseProtocol[_EstimateP]": ...

    def estimated_price(
        self,
        symbol: str,
        side: Literal["bid", "ask", "both"],
        *quantity: Union[float, str, int],
        create_namespace: bool = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponse[Union[_EstimateP, _EstimateD]]":
        return self.make_json_api_request(
            "api/v1/crypto/marketdata/estimated_price/",
            params={
                "symbol": symbol,
                "side": side,
                "quantity": ",".join((str(q) for q in quantity)),
            },
            create_namespace=create_namespace,
            **kwargs,
        )


__all__ = ["MarketMixin"]
