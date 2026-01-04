"""
NOTICE: This module is not yet complete and may change without notice.
"""

import json
import urllib.parse
import uuid
from typing import TYPE_CHECKING, Optional, Literal, Dict, Union, Unpack

from .. import constants as _constants
from .._protocols import Client as _Client
from ... import schema as _base_schema
from ...schema import trading as _schema

if TYPE_CHECKING:
    from .. import structures as _structs


ORDER_REQUIREMENTS = {
    "market": tuple(),
    "limit": ("limit_price",),
    "stop_loss": ("stop_price", "time_in_force"),
    "stop_limit": ("limit_price", "stop_price", "time_in_force"),
}


class TradingMixin(_Client):

    def trading_pairs(
        self,
        *symbols: str,
        **kwargs: "Unpack[_structs.ClientOptions]",
    ) -> "_structs.APIResponse[_schema.TradingPairResults]":
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/trading_pairs/",
            params={"symbol": list(symbols)},
            success_schema=_schema.TradingPairResults,
            **kwargs,
        )

    def holdings(
        self,
        *asset_code: str,
        **kwargs: "Unpack[_structs.ClientOptions]",
    ) -> "_structs.APIResponse[_schema.HoldingResults]":
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/holdings/",
            params={"asset_code": list(asset_code)},
            success_schema=_schema.HoldingResults,
            **kwargs,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin,too-many-arguments,too-many-positional-arguments,too-many-locals
    def orders(
        self,
        created_at_start: Optional[str] = None,
        created_at_end: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        side: Optional[Literal["buy", "sell"]] = None,
        state: Optional[
            Literal["open", "cancelled", "partially_filled", "filled", "failed"]
        ] = None,
        type: Optional[Literal["limit", "market", "stop_limit", "stop_loss"]] = None,
        updated_at_start: Optional[str] = None,
        updated_at_end: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        **kwargs: "Unpack[_structs.ClientOptions]",
    ) -> "_structs.APIResponse[_schema.OrderResults]":
        # Create our parameters
        params = {}

        # fmt: off
        for param_name, param_value in (
            ("created_at_start", created_at_start), ("created_at_end", created_at_end),
            ("symbol", symbol), ("id", id), ("side", side), ("state", state), ("type", type),
            ("updated_at_start", updated_at_start), ("updated_at_end", updated_at_end),
            ("cursor", cursor), ("limit", limit),
        ):
            # fmt: on
            if param_value is not None:
                params[param_name] = param_value

        return self.make_parsed_api_request(
            "api/v1/crypto/trading/orders/",
            params=params,
            success_schema=_schema.OrderResults,
            **kwargs,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    def order(
        self,
        symbol: str,
        side: Literal["buy", "sell"],
        type: Literal["limit", "market", "stop_limit", "stop_loss"],
        asset_quantity: Optional[float] = None,
        client_order_id: Optional[str] = None,
        quote_amount: Optional[float] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: Optional[Literal["gtc", "gfd", "gfw", "gfm"]] = None,
        **kwargs: "Unpack[_structs.ClientOptions]",
    ) -> "_structs.APIResponse[_schema.Order]":
        if type not in ORDER_REQUIREMENTS:
            raise ValueError(f"Unknown order type {type}")

        order_config: Dict[str, Union[str, int, float]] = {}
        if asset_quantity is not None:
            order_config["asset_quantity"] = asset_quantity
        elif quote_amount is not None:
            if type == "market":
                raise ValueError("Cannot specify quote amount for market orders")

            order_config["quote_amount"] = quote_amount
        else:
            raise ValueError("Must specify either asset quantity or quote amount")

        for payload_key, payload_value in (
            ("limit_price", limit_price),
            ("stop_price", stop_price),
            ("time_in_force", time_in_force),
        ):
            if payload_value is None:
                if payload_key in ORDER_REQUIREMENTS[type]:
                    raise ValueError(
                        f"Missing required key {payload_key} for order type {type}"
                    )

                continue

            if payload_key not in ORDER_REQUIREMENTS[type]:
                raise ValueError(f"Unexpected key {payload_key} for order type {type}")

            order_config[payload_key] = payload_value

        return self.make_parsed_api_request(
            f"api/v1/crypto/trading/orders/",
            body=json.dumps(
                {
                    "symbol": symbol,
                    "client_order_id": client_order_id or str(uuid.uuid4()),
                    "side": side,
                    "type": type,
                    f"{type}_order_config": order_config,
                }
            ),
            success_schema=_schema.Order,
            method=_constants.RequestMethod.POST,
            **kwargs,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    def cancel(
        self,
        id: str,
        **kwargs: "Unpack[_structs.ClientOptions]",
    ) -> "_structs.APIResponse[_base_schema.Message]":
        return self.make_api_request(
            f"api/v1/crypto/trading/orders/{urllib.parse.quote(id)}/cancel/",
            method=_constants.RequestMethod.POST,
            **kwargs,
        )


__all__ = ["TradingMixin"]
