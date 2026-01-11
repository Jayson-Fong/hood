"""
NOTICE: This module is not yet complete and may change without notice.
"""

import json
import urllib.parse
import uuid
from typing import TYPE_CHECKING, Optional, Literal, Dict, Union, overload

from .. import constants as _constants
from .._protocols import Client as _Client
from ..schema import trading as _schema

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
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.TradingPairResults]":
        """
        Retrieve trading pair information filtered by the provided symbol(s).

        Args:
            *symbols: One or more trading pair symbols to filter the results in all uppercase.
            limit: Maximum number of results to return.
            cursor: Pagination cursor to continue a previous listing.

        Returns:
            Trading pairs on success or error.
        """

        params: "_structs.QueryParams" = {"symbol": list(symbols)}

        # fmt: off
        for param_name, param_value in (
            ("limit", limit), ("cursor", cursor),
        ):
            # fmt: on
            if param_value is not None:
                params[param_name] = param_value

        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/trading_pairs/",
            params=params,
            success_schema=_schema.TradingPairResults,
            error_schema=_schema.Errors,
        )

    def holdings(
        self,
        *asset_code: str,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.HoldingResults]":
        """
        Retrieve holdings information for the given asset codes with optional pagination.

        Args:
            *asset_code: One or more asset codes to query, all in uppercase (ex: BTC).
            limit: Maximum number of results to return.
            cursor: Cursor for paginated results.

        Returns:
            API response containing holdings matching the requested asset codes or an error.
        """

        params: "_structs.QueryParams" = {"asset_code": list(asset_code)}

        # fmt: off
        for param_name, param_value in (
            ("limit", limit), ("cursor", cursor),
        ):
            # fmt: on
            if param_value is not None:
                params[param_name] = param_value

        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/holdings/",
            params=params,
            success_schema=_schema.HoldingResults,
            error_schema=_schema.Errors,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin,too-many-arguments,too-many-positional-arguments,too-many-locals
    def orders(
        self,
        *,
        created_at_start: Optional[str] = None,
        created_at_end: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        side: Optional[Literal["buy", "sell"]] = None,
        state: Optional[
            Literal["open", "canceled", "partially_filled", "filled", "failed"]
        ] = None,
        type: Optional[Literal["limit", "market", "stop_limit", "stop_loss"]] = None,
        updated_at_start: Optional[str] = None,
        updated_at_end: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.OrderResults]":
        """
        Retrieve a list of orders filtered by the given criteria.

        Args:
            created_at_start: Include orders created at or after this timestamp.
            created_at_end: Include orders created at or before this timestamp.
            symbol: Filter orders for the given trading symbol.
            id: Filter to a specific order id.
            side: Filter by order side.
            state: Filter by order state.
            type: Filter by order type.
            updated_at_start: Include orders updated at or after this timestamp.
            updated_at_end: Include orders updated at or before this timestamp.
            cursor: Pagination cursor to fetch the next page of results.
            limit: Maximum number of results to return.

        Returns:
            Parsed order results on success or _schema.Errors on failure.
        """

        # Create our parameters
        params: "_structs.QueryParams" = {}

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

        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/orders/",
            params=params,
            success_schema=_schema.OrderResults,
            error_schema=_schema.Errors,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["limit"],
        asset_quantity: float,
        limit_price: float,
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a limit order for the specified trading symbol.

        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD").
            side: Order side.
            asset_quantity: Quantity of the base asset to buy or sell.
            limit_price: Limit price per unit in the quote currency.
            client_order_id: Optional client-provided identifier; a UUID will be generated if omitted.

        Returns:
            n API response containing the created `Order` on success or error on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["limit"],
        quote_amount: float,
        limit_price: float,
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a limit order using a quote-currency amount.

        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD").
            side: Order side.
            type: Order type; must be "limit" for this signature.
            quote_amount: Amount in the quote currency to execute (the total spend or receive).
            limit_price: Limit price per unit of the base asset.
            client_order_id: Optional client-provided identifier; if omitted, a UUID is generated.

        Returns:
            The API response wrapping the created Order on success, or error on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["market"],
        asset_quantity: float,
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a market order for the given trading symbol.

        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD").
            side: Order direction.
            asset_quantity: Quantity of the base asset to buy or sell.
            client_order_id: Client-provided identifier for the order; if omitted, one is generated.

        Returns:
            API response containing the created Order on success, or error on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["stop_limit"],
        asset_quantity: float,
        limit_price: float,
        stop_price: float,
        time_in_force: Literal["gtc", "gfd", "gfw", "gfm"],
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a stop-limit order for the given trading pair.

        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD").
            side: Order direction.
            type: Order type; this signature requires a stop-limit order.
            asset_quantity: Quantity of the base asset to buy or sell.
            limit_price: Limit price that becomes active once the stop price is reached.
            stop_price: Trigger price that activates the limit order.
            time_in_force: Time-in-force instruction for the resulting limit order.
            client_order_id: Optional client-provided order identifier; if omitted, a UUID is generated.

        Returns:
            API response containing the created Order on success or error on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["stop_limit"],
        quote_amount: float,
        limit_price: float,
        stop_price: float,
        time_in_force: Literal["gtc", "gfd", "gfw", "gfm"],
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a stop-limit order for the given trading symbol.

        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD").
            side: Order side, either "buy" or "sell".
            quote_amount: Amount expressed in the quote currency to place for the order.
            limit_price: Limit price to execute the order once the stop is triggered.
            stop_price: Stop price that, when reached, activates the limit order.
            time_in_force: Time-in-force directive; one of "gtc", "gfd", "gfw", or "gfm".
            client_order_id: Optional client-specified identifier; generated automatically if omitted.

        Returns:
            API response containing the created Order on success or Errors on failure.

        Raises:
            ValueError: If provided fields are invalid for a stop-limit order.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["stop_loss"],
        asset_quantity: float,
        stop_price: float,
        time_in_force: Literal["gtc", "gfd", "gfw", "gfm"],
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a stop-loss order for the specified trading symbol.

        Args:
            symbol: Trading pair symbol to place the order for.
            side: Order side.
            asset_quantity: Quantity of the asset to buy or sell.
            stop_price: Trigger price for the stop-loss order.
            time_in_force: Order time-in-force policy.
            client_order_id: Cclient-supplied identifier.

        Returns:
            API response containing an `Order` on success or error on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    @overload
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["stop_loss"],
        quote_amount: float,
        stop_price: float,
        time_in_force: Literal["gtc", "gfd", "gfw", "gfm"],
        client_order_id: Optional[str] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a stop-loss order specified by a quote-denominated amount.

        Args:
            symbol: Trading symbol for the order (e.g., "BTC-USD").
            side: Order side, either "buy" or "sell".
            quote_amount: Amount in the quote currency to fill.
                Mutually exclusive with `asset_quantity`.
            stop_price: Trigger price at which the stop-loss order becomes active.
            time_in_force: Order time-in-force policy ("gtc", "gfd", "gfw", "gfm").
            client_order_id: Optional client-provided identifier;
                if omitted, a UUID will be generated.

        Returns:
            API response containing the created order on success or error details on failure.
        """

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    def order(
        self,
        symbol: str,
        *,
        side: Literal["buy", "sell"],
        type: Literal["limit", "market", "stop_limit", "stop_loss"],
        asset_quantity: Optional[float] = None,
        client_order_id: Optional[str] = None,
        quote_amount: Optional[float] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: Optional[Literal["gtc", "gfd", "gfw", "gfm"]] = None,
    ) -> "_structs.MaybeAPIResponse[_schema.Order]":
        """
        Create a new crypto order for the given symbol using a type-specific order configuration.

        Args:
            symbol: Trading symbol for the order.
            side: Order side.
            type: Order type that determines required and allowed config keys.
            asset_quantity: Quantity of the base asset to trade.
                Mutually exclusive with `quote_amount`.
            client_order_id: Client identifier for the order.
                If omitted, a UUID will be generated.
            quote_amount: Quote amount. Mutually exclusive with `asset_quantity`.
            limit_price: Limit price; required or disallowed depending on `type`.
            stop_price: Stop trigger price; required or disallowed depending on `type`.
            time_in_force: Time-in-force policy; required or disallowed depending on `type`.

        Returns:
            Parsed API response containing the created `Order` on success or `Errors` on failure.
        """

        if type not in ORDER_REQUIREMENTS:
            raise ValueError(f"Unknown order type {type}")

        if asset_quantity is not None and quote_amount is not None:
            raise ValueError("Cannot specify both asset quantity and quote amount")

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

        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            "api/v1/crypto/trading/orders/",
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
            error_schema=_schema.Errors,
            method=_constants.RequestMethod.POST,
        )

    # noinspection PyShadowingBuiltins
    # pylint: disable=redefined-builtin
    def cancel(
        self,
        id: str,
    ) -> "_structs.MaybeAPIResponse[_schema.Message]":
        """
        Cancel an existing order by its identifier.

        Args:
            id: The order identifier to cancel.

        Returns:
            Message on successful cancellation or error details on failure.
        """

        # noinspection PyTypeChecker
        return self.make_parsed_api_request(
            f"api/v1/crypto/trading/orders/{urllib.parse.quote(id)}/cancel/",
            method=_constants.RequestMethod.POST,
            success_schema=_schema.Message,
            error_schema=_schema.Errors,
        )


__all__ = ["TradingMixin"]
