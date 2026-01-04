# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class TradingAccountDetail:
    account_number: Optional[str] = None
    status: Optional[Literal["active", "deactivated", "sell_only"]] = None
    buying_power: Optional[str] = None
    buying_power_currency: Optional[str] = None
