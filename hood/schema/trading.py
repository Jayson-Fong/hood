from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal, List, Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class TradingPair:
    asset_code: Optional[str] = None
    quote_code: Optional[str] = None
    quote_increment: Optional[str] = None
    asset_increment: Optional[str] = None
    max_order_size: Optional[str] = None
    min_order_size: Optional[str] = None
    # noinspection SpellCheckingInspection
    status: Optional[Literal["tradable", "untradable", "sellonly"]] = None
    symbol: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class TradingPairResults:
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[TradingPair] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class Holding:
    account_number: Optional[str] = None
    asset_code: Optional[str] = None
    total_quantity: Optional[Decimal] = None
    quantity_available_for_trading: Optional[Decimal] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class HoldingResults:
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Holding] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderExecution:
    effective_price: Optional[str] = None
    quantity: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class MarketOrderConfig:
    asset_quantity: Optional[Decimal] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class LimitOrderConfig:
    quote_amount: Optional[Decimal] = None
    asset_quantity: Optional[Decimal] = None
    limit_price: Optional[Decimal] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class StopLossOrderConfig:
    quote_amount: Optional[Decimal] = None
    asset_quantity: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
    time_in_force: Optional[Literal["gtc", "gfd", "gfw", "gfm"]] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class StopLimitOrderConfig:
    quote_amount: Optional[Decimal] = None
    asset_quantity: Optional[Decimal] = None
    limit_price: Optional[str] = None
    stop_price: Optional[Decimal] = None
    time_in_force: Optional[Literal["gtc", "gfd", "gfw", "gfm"]] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Order:
    id: Optional[str] = None
    account_number: Optional[str] = None
    symbol: Optional[str] = None
    client_order_id: Optional[str] = None
    side: Optional[Literal["buy", "sell"]] = None
    executions: List[OrderExecution] = field(default_factory=list)
    type: Optional[Literal["limit", "market", "stop_limit", "stop_loss"]] = None
    state: Optional[
        Literal["open", "cancelled", "partially_filled", "filled", "failed"]
    ] = None
    average_price: Optional[Decimal] = None
    filled_asset_quantity: Optional[Decimal] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    market_order_config: Optional[MarketOrderConfig] = None
    limit_order_config: Optional[LimitOrderConfig] = None
    stop_loss_order_config: Optional[StopLossOrderConfig] = None
    stop_limit_order_config: Optional[StopLimitOrderConfig] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderResults:
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Order] = field(default_factory=list)


__all__ = [
    "TradingPair",
    "TradingPairResults",
    "Holding",
    "HoldingResults",
    "OrderExecution",
    "MarketOrderConfig",
    "LimitOrderConfig",
    "StopLossOrderConfig",
    "StopLimitOrderConfig",
    "Order",
    "OrderResults",
]
