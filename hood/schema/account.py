from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class TradingAccountDetail:
    account_number: Optional[str] = None
    status: Optional[Literal["active", "deactivated", "sell_only"]] = None
    buying_power: Optional[Decimal] = None
    buying_power_currency: Optional[str] = None
