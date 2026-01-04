from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal, List, Optional

from . import Errors


@dataclass(frozen=True, slots=True, kw_only=True)
class BestBidAsk:
    symbol: Optional[str] = None
    price: Optional[Decimal] = None
    bid_inclusive_of_sell_spread: Optional[Decimal] = None
    sell_spread: Optional[Decimal] = None
    ask_inclusive_of_buy_spread: Optional[Decimal] = None
    buy_spread: Optional[Decimal] = None
    timestamp: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class BestBidAskResults:
    results: List[BestBidAsk] = field(default_factory=list)


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True, slots=True, kw_only=True)
class MarketEstimate:
    symbol: Optional[str] = None
    side: Optional[Literal["bid", "ask"]] = None
    price: Optional[Decimal] = None
    quantity: Optional[Decimal] = None
    bid_inclusive_of_sell_spread: Optional[Decimal] = None
    sell_spread: Optional[Decimal] = None
    ask_inclusive_of_buy_spread: Optional[Decimal] = None
    buy_spread: Optional[Decimal] = None
    timestamp: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class MarketEstimateResults:
    results: List[MarketEstimate] = field(default_factory=list)


__all__ = ["Errors", "BestBidAskResults", "MarketEstimateResults"]
