from typing import Protocol, Literal, TypedDict, List, TypeVar, Generic


# Result Structure


T = TypeVar("T")


# pylint: disable=too-few-public-methods
class ResultsResponseProtocol(Protocol[T]):
    results: List[T]


class ResultsResponseDict(TypedDict, Generic[T]):
    results: List[T]


# pylint: disable=too-few-public-methods
class ResultPageResponseProtocol(Protocol[T]):
    next: str
    previous: str
    results: List[T]


class ResultPageResponseDict(TypedDict, Generic[T]):
    next: str
    previous: str
    results: List[T]


# Account


# pylint: disable=too-few-public-methods
class TradingAccountDetailProtocol(Protocol):
    account_number: str
    status: Literal["active", "deactivated", "sell_only"]
    buying_power: str
    buying_power_currency: str


class TradingAccountDetailDict(TypedDict):
    account_number: str
    status: Literal["active", "deactivated", "sell_only"]
    buying_power: str
    buying_power_currency: str


# Market -> Best Bid Ask


# pylint: disable=too-few-public-methods
class _BestBidAskResultProtocol(Protocol):
    symbol: str
    price: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    timestamp: str


# pylint: disable=invalid-name
BestBidAskProtocol = ResultsResponseProtocol[_BestBidAskResultProtocol]


class _BestBidAskResultDict(TypedDict):
    symbol: str
    price: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    timestamp: str


# pylint: disable=invalid-name
BestBidAskDict = ResultsResponseDict[_BestBidAskResultDict]


# pylint: disable=too-few-public-methods
class _MarketEstimateResultProtocol(Protocol):
    symbol: str
    side: Literal["bid", "ask"]
    price: float
    quantity: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    timestamp: str


# pylint: disable=invalid-name
MarketEstimateProtocol = ResultsResponseProtocol[_MarketEstimateResultProtocol]


class _MarketEstimateResultDict(TypedDict):
    symbol: str
    side: Literal["bid", "ask"]
    price: float
    quantity: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    timestamp: str


# pylint: disable=invalid-name
MarketEstimateDict = ResultsResponseDict[_MarketEstimateResultDict]


__all__ = [
    "TradingAccountDetailProtocol",
    "TradingAccountDetailDict",
    "BestBidAskProtocol",
    "BestBidAskDict",
    "MarketEstimateProtocol",
    "MarketEstimateDict",
]
