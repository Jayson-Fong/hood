from dataclasses import dataclass, field
from typing import Literal, List, Optional


# pylint: disable=too-few-public-methods
@dataclass
class BestBidAsk:
    symbol: Optional[str] = None
    price: Optional[float] = None
    bid_inclusive_of_sell_spread: Optional[float] = None
    sell_spread: Optional[float] = None
    ask_inclusive_of_buy_spread: Optional[float] = None
    buy_spread: Optional[float] = None
    timestamp: Optional[str] = None


@dataclass
class BestBidAskResults:
    results: List[BestBidAsk] = field(default_factory=list)


@dataclass
class MarketEstimate:
    symbol: Optional[str] = None
    side: Optional[Literal["bid", "ask"]] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    bid_inclusive_of_sell_spread: Optional[float] = None
    sell_spread: Optional[float] = None
    ask_inclusive_of_buy_spread: Optional[float] = None
    buy_spread: Optional[float] = None
    timestamp: Optional[str] = None


@dataclass
class MarketEstimateResults:
    results: List[MarketEstimate] = field(default_factory=list)


__all__ = ["BestBidAskResults", "MarketEstimateResults"]
