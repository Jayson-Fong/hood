from typing import TYPE_CHECKING, Optional, Literal

from .._protocols import Client as _Client

if TYPE_CHECKING:
    from .. import structures as _structs


class TradingMixin(_Client):

    def trading_pairs(
        self,
        *symbols: str,
        create_namespace: bool = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponse":
        return self.make_json_api_request(
            "api/v1/crypto/trading/trading_pairs/",
            params={"symbol": list(symbols)},
            create_namespace=create_namespace,
            **kwargs,
        )

    def holdings(
        self,
        *symbols: str,
        create_namespace: bool = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponse":
        return self.make_json_api_request(
            "api/v1/crypto/trading/holdings/",
            params={"asset_code": list(symbols)},
            create_namespace=create_namespace,
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
        create_namespace: bool = False,
        **kwargs,
    ) -> "_structs.MaybeAPIResponse":
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

        return self.make_json_api_request(
            "api/v1/crypto/trading/orders/",
            params=params,
            create_namespace=create_namespace,
            **kwargs,
        )


__all__ = ["TradingMixin"]
