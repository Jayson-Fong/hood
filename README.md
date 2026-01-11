<!--suppress HtmlDeprecatedAttribute-->
<div align="center">
   <h1>🪶 hood</h1>

</div>

<hr />

<div align="center">

[💼 Purpose](#purpose) | [🛠️️ Installation](#installation) | [🏁 Usage](#usage) | [🛡️ Disclaimers](#disclaimers)

</div>

<hr />

# Purpose

This package seeks to provide a client for the official 
[Robinhood Crypto API](https://docs.robinhood.com/crypto/trading/) for viewing Robinhood crypto account and market 
details alongside performing trading activities. It does _not_ incorporate endpoints to interact with Robinhood's 
undocumented brokerage API.

While [Robinhood itself provides a sample client](https://docs.robinhood.com/crypto/trading/#section/Getting-Started), 
it does not provide any type hinting for its API's possible return types, types for order configuration, or methods to 
handle pagination.

The development of this package is **not affiliated with Robinhood**.

# Installation

The latest development release is installable from GitHub:

```shell
python3 -m pip install git+https://github.com/Jayson-Fong/hood
```

# Usage

## Authentication

Usage of the Crypto Trading API requires registering an Ed25519 key with your Robinhood account to acquire an API key. 
API keys are used in conjunction with the Ed25519 key to securely sign your requests to Robinhood and include a
timestamp as part of the signed message to mitigate the risk of replay attacks.

> [!NOTE]  
> Signed requests to Robinhood are generally valid for up to 30 seconds following generation. While this package
> sends requests immediately following signature generation, poor network performance or time synchronization issues may
> lead to issues authenticating with Robinhood.

> [!CAUTION]
> While Robinhood will generally reject signed messages 30 seconds after timestamp generation, this may allow for replay
> attacks. To mitigate this risk, only perform trading activities on networks you trust and do not share your API key
> or private key.

You can generate a private key using the following:

```python
import base64
from hood.crypto_trading import auth

private_key = auth.Credential.generate()

private_key_base64 = base64.b64encode(private_key.encode()).decode()
public_key_base64 = base64.b64encode(private_key.verify_key.encode()).decode()

print("Private Key (Base64):", private_key_base64, sep="\n\t")
print("Public Key (Base64):", public_key_base64, sep="\n\t")
```

This will output in the following format:

```plaintext
Private Key (Base64):
        AmkImtzGG3lW5BKXhqvJTxvFfL3gFqrRsOI9U/6d6CA=
Public Key (Base64):
        XnMFEPYylcEYm64Z3S7B8JfrexlxHzP1p+eD/mJ4gSI=
```

**Do not** share your private key or provide it to Robinhood. If you intend to use `hood` on multiple devices, it is
recommended that you generate a unique key pair for each device.

You will need to provide your public key to Robinhood to generate an API key and associate it with your account. To
locate the form:

1. Navigate to account settings
2. Open the `Crypto` settings tab
3. Under `API Trading`, click `Add key`

> [!NOTE]  
> To ensure your account's security, consider restricting permissions on a 
> [least-privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) basis. By granting API access, you
> should assume that your crypto account ID will always be accessible.

Keep your generated private key and the API key in a secure location as they are required for accessing the Crypto 
Trading API.

## API Client

Requests go through a client instance. The built-in client is `hood.crypto_trading:CryptoTradingClient`. It can be 
instantiated as follows given a private key.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
```

A `hood.crypto_trading.auth:Credential` instance can be instantiated using an API key and a private key. The
private key may either be an instance of `nacl.signing:SigningKey` (from `PyNaCl`) or bytes. If you have your
private key in the form of Base64, it can be converted into bytes:

```python
import base64

private_key_seed = base64.b64decode("BASE64_PRIVATE_KEY_HERE")
```

When using `hood`"s dedicated methods to make requests against Robinhood"s Crypto Trading API, the function caller
will receive an instance of `hood.structures.APIResponse`, containing the following attributes:

- data (`None` or Dataclass Instance): Parsed response data.
- response (`None` or `requests.Response`): Response from the Crypto Trading API.
- error (`BaseException`): Exception if one was raised while processing the request.

### Account Endpoints

<details>
<summary>Get Crypto Trading Account Details</summary>

Get the Robinhood Crypto Trading account details associated with the authenticated user.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.accounts()
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.account

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.account.TradingAccountDetail(
        account_number="000000000000",
        status="active",
        buying_power=decimal.Decimal("000.0000"),
        buying_power_currency="USD",
    ),
    response=requests.Response(),
    error=None
)
```

</details>


### Market Data Endpoints

<details>
<summary>Get Best Price</summary>

Fetch a single `bid` and `ask` price for each symbol specified. Multiple symbols may be specified as additional arguments.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.best_bid_ask("BTC-USD", "ETH-USD")
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.market

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.market.BestBidAskResults(
        results=[
            hood.crypto_trading.schema.market.BestBidAsk(
                symbol="BTC-USD",
                price=decimal.Decimal("94200.49475077"),
                bid_inclusive_of_sell_spread=decimal.Decimal("93401.43950154"),
                sell_spread=decimal.Decimal("0.0084825"),
                ask_inclusive_of_buy_spread=decimal.Decimal("94999.55"),
                buy_spread=decimal.Decimal("0.0084825"),
                timestamp="2026-01-05T21:04:16.35583523Z",
            ),
            hood.crypto_trading.schema.market.BestBidAsk(
                symbol="ETH-USD",
                price=decimal.Decimal("3247.68922388"),
                bid_inclusive_of_sell_spread=decimal.Decimal("3220.746636"),
                sell_spread=decimal.Decimal("0.00829593"),
                ask_inclusive_of_buy_spread=decimal.Decimal("3274.63181176"),
                buy_spread=decimal.Decimal("0.00829593"),
                timestamp="2026-01-05T21:04:16.355835525Z",
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

This endpoint may return an error response. For example, when providing an invalid symbol.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.best_bid_ask("BTC-USD", "ETH-US")
```

Expected output structure for response code `400`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.market

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.market.Errors(
    type="validation_error",
    errors=[
        hood.crypto_trading.schema.market.Error(
            detail="Invalid symbol: ETH-US",
            attr="symbol",
      ),
    ],
  ),
  response=requests.Response(), 
  error=None,
)
```

</details>

<details>
<summary>Get Estimated Price</summary>

Requests the estimated price for a symbol. A single symbol is required, to be followed by the side. Valid sides are: 
`bid`, `ask`, `both`. Quantities may be specified as additional arguments. The Robinhood Crypto Trading API accepts up
to 10 quantities. The quantity may be passed as a float, string, integer, or `decimal.Decimal`. Quantities are converted
to a string using `str(quantity)`.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.estimated_price("BTC-USD", "both", 0.1, "1")
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.market

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.market.MarketEstimateResults(
        results=[
            hood.crypto_trading.schema.market.MarketEstimate(
                symbol="BTC-USD",
                side="bid",
                price=decimal.Decimal("94110.38097125"),
                quantity=decimal.Decimal("0.1"),
                bid_inclusive_of_sell_spread=decimal.Decimal("93311.1019425"),
                sell_spread=decimal.Decimal("0.008493"),
                ask_inclusive_of_buy_spread=None,
                buy_spread=None,
                timestamp="2026-01-05T16:08:10.270830931-05:00",
            ),
            hood.crypto_trading.schema.market.MarketEstimate(
                symbol="BTC-USD",
                side="ask",
                price=decimal.Decimal("94110.38097125"),
                quantity=decimal.Decimal("0.1"),
                bid_inclusive_of_sell_spread=None,
                sell_spread=None,
                ask_inclusive_of_buy_spread=decimal.Decimal("94909.66"),
                buy_spread=decimal.Decimal("0.008493"),
                timestamp="2026-01-05T16:08:10.270830931-05:00",
            ),
            hood.crypto_trading.schema.market.MarketEstimate(
                symbol="BTC-USD",
                side="bid",
                price=decimal.Decimal("94109.17804723"),
                quantity=decimal.Decimal("1"),
                bid_inclusive_of_sell_spread=decimal.Decimal("93307.82609446"),
                sell_spread=decimal.Decimal("0.00851513"),
                ask_inclusive_of_buy_spread=None,
                buy_spread=None,
                timestamp="2026-01-05T16:08:10.270830931-05:00",
            ),
            hood.crypto_trading.schema.market.MarketEstimate(
                symbol="BTC-USD",
                side="ask",
                price=decimal.Decimal("94109.17804723"),
                quantity=decimal.Decimal("1"),
                bid_inclusive_of_sell_spread=None,
                sell_spread=None,
                ask_inclusive_of_buy_spread=decimal.Decimal("94910.53"),
                buy_spread=decimal.Decimal("0.00851513"),
                timestamp="2026-01-05T16:08:10.270830931-05:00",
            ),
        ]
    ),
    response=requests.Response(),
    error=None,
)
```

This endpoint may return an error response. For example, when providing an invalid symbol.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.estimated_price("BTC-USD", "both", 0.1, "1")
```

Expected output structure for response code `400`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.market

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.market.Errors(
        type="server_error",
        errors=[
            hood.crypto_trading.schema.market.Error(
                detail="Internal server error", 
                attr=None,
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

</details>

### Trading Endpoints

<details>
<summary>Get Crypto Trading Pairs</summary>

Fetch a list of trading pairs. Multiple symbols may be specified as additional arguments. You may pass an integer
`limit` to limit the number of results in one page. If iterating through pages, a string `cursor` may be passed
as a keyword argument. If no symbols are specified, all symbols will be returned.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.trading_pairs("BTC-USD", "ETH-USD")
```

Expected output structure for response code `200`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.TradingPairResults(
        next=None,
        previous=None,
        results=[
            hood.crypto_trading.schema.trading.TradingPair(
                asset_code="ETH", 
                quote_code="USD", 
                quote_increment="0.010000000000000000", 
                asset_increment="0.000001000000000000", 
                max_order_size="280.0000000000000000", 
                min_order_size="0.000100000000000000", 
                status="tradable", 
                symbol="ETH-USD",
            ),
            hood.crypto_trading.schema.trading.TradingPair(
              asset_code="BTC",
              quote_code="USD",
              quote_increment="0.010000000000000000",
              asset_increment="0.000000010000000000",
              max_order_size="20.0000000000000000",
              min_order_size="0.000001000000000000",
              status="tradable",
              symbol="BTC-USD",
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

If paging, a `next` and `previous` URL may be provided in the form of a string.

This endpoint may return an error response. For example, when providing an invalid symbol.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.trading_pairs("BTC-USD", "ETH-US")
```

Expected output structure for response code `400` and `404`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Errors(
        type="validation_error",
        errors=[
            hood.crypto_trading.schema.trading.Error(
                detail="Select a valid choice.",
                attr='symbol',
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

</details>

<details>
<summary>Get Crypto Holdings</summary>

Details the holdings in your Crypto Trading account. Omit asset codes to list all holdings. Multiple asset codes may
be passed as positional arguments, all uppercase. An integer `limit` keyword argument may be set to limit the number of
results per page. If paging, the cursor may be passed in a `cursor` keyword argument.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
# noinspection SpellCheckingInspection
client.holdings("USDC")
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

# noinspection SpellCheckingInspection
hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.HoldingResults(
        next=None,
        previous=None,
        results=[
            hood.crypto_trading.schema.trading.Holding(
                account_number="000000000000",
                asset_code="USDC", 
                total_quantity=decimal.Decimal("1.000000000000000000"),
                quantity_available_for_trading=decimal.Decimal("1.000000000000000000"),
            ),
        ],
    ), 
  response=requests.Response(),
  error=None,
)
```

If paging, a `next` and `previous` URL may be provided in the form of a string.

This endpoint may return an error response. For example, when providing an invalid cursor.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.holdings(cursor="0")
```

Expected output structure for response code `400` and `404`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Errors(
        type="client_error", 
        errors=[
            hood.crypto_trading.schema.trading.Error(
                detail="Not found.",
                attr=None
            ),
        ],
    ),
    response=requests.Response(), 
    error=None,
)
```

</details>

<details>
<summary>Get Crypto Orders</summary>

Multiple types of orders are supported with different parameters. The client supports the following order
types, specified through the `type` parameter, along with their required parameters:

* limit
  * quote_amount (float)
  * asset_quantity (float)
  * limit_price (float)
* market
  * asset_quantity (float)
* stop_limit
  * quote_amount (float)
  * asset_quantity (float)
  * limit_price (float)
  * stop_price (float)
  * time_in_force (str: gtc, gfd, gfw, gfm)
* stop_loss
  * quote_amount (float)
  * asset_quantity (float)
  * limit_price (float)
  * stop_price (float)
  * time_in_force (str: gtc, gfd, gfw, gfm)

All order types require a currency pair symbol such as `BTC-USD`, accepted as a positional parameter. Only a single
currency pair symbol is supported.

For order types that accept both a `quote_amount` and a `asset_quantity`, you may only specify either `quote_amount` or
`asset_quantity` - not both simultaneously. All methods accept a `side`, which must be either `buy` or `sell`, and you
may optionally provide a `client_order_id`, a UUID for client reference. If a `client_order_id` is not specified, one
will be automatically generated.

If you intend on modifying the order using the library, it is suggested that you provide a `client_order_id` so that
it is immediately consumable, such as for order cancellation. Otherwise, the automatically generated value is only
available through the response.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.orders(limit=1)
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.OrderResults(
        next="https://trading.robinhood.com/api/v1/crypto/trading/orders/?cursor=00000000000000000000000000000000000000000000000000000000&limit=1",
        previous=None,
        results=[
            hood.crypto_trading.schema.trading.Order(
                id="faceaa50-0756-4a5e-b4e4-34e7b550ecec",
                account_number="000000000000",
                symbol="BTC-USD",
                client_order_id="440f4b24-4bd8-4c80-97e2-003886963970",
                side="buy",
                executions=[],
                type="limit",
                state="canceled",
                average_price=None,
                filled_asset_quantity=decimal.Decimal("0E-18"),
                created_at="2026-01-10T21:03:29.896079-05:00",
                updated_at="2026-01-10T21:03:48.484410-05:00",
                market_order_config=None,
                limit_order_config=hood.crypto_trading.schema.trading.LimitOrderConfig(
                    quote_amount=None,
                    asset_quantity=decimal.Decimal("0.000100000000000000"),
                    limit_price=decimal.Decimal("90000.000000000000000000"),
                ),
                stop_loss_order_config=None,
                stop_limit_order_config=None,
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

If paging, a `next` and `previous` URL may be provided in the form of a string.

This endpoint may return an error response. For example, when providing an invalid cursor.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.orders(limit=1)
```

Expected output structure for response code `400` and `404`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Errors(
        type="client_error",
        errors=[
            hood.crypto_trading.schema.trading.Error(
                detail="Not found.",
                attr=None,
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

</details>

<details>
<summary>Place New Crypto Order</summary>

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.order("USDC-USD", side="buy", type="market", asset_quantity=0.01)
```

Expected output structure for response code `200`:

```python
import decimal
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Order(
        id="296217b3-febe-4f27-a6d4-7ee569564d4d",
        account_number="000000000000",
        symbol="USDC-USD",
        client_order_id="28055f9f-252e-4012-9e34-af93e1c00703",
        side="buy",
        executions=[],
        type="market",
        state="open",
        average_price=None,
        filled_asset_quantity=decimal.Decimal("0E-18"),
        created_at="2026-01-10T20:50:13.931262-05:00",
        updated_at="2026-01-10T20:50:14.362428-05:00",
        market_order_config=hood.crypto_trading.schema.trading.MarketOrderConfig(
            asset_quantity=decimal.Decimal("0.010000000000000000"),
        ),
        limit_order_config=None,
        stop_loss_order_config=None,
        stop_limit_order_config=None,
    ),
    response=requests.Response(),
    error=None,
)
```

This endpoint may return an error response. For example, when the asset quantity is outside the supported range.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.order("USDC-USD", side="buy", type="market", asset_quantity=1000000)
```

Expected output structure for response code `400`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Errors(
        type="validation_error",
        errors=[
            hood.crypto_trading.schema.trading.Error(
                detail="must be less than or equal to 250000.0000000000000000",
                attr="market_order_config.asset_quantity",
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

</details>

<details>
<summary>Cancel Open Crypto Order</summary>

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.cancel("cc9c89d6-dea4-4dab-8354-0994e1cd080a")
```

Expected output structure for response code `200`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Message(
        body='"Cancel request has been submitted for order cc9c89d6-dea4-4dab-8354-0994e1cd080a"',
    ),
    response=requests.Response(),
    error=None,
)
```

This endpoint may return an error response. For example, when it is not possible to cancel an order.

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.cancel("cc9c89d6-deaa-4dab-8354-0994e1cd080a")
```

Expected output structure for response code `400` and `404`:

```python
import requests
import hood.crypto_trading.structures
import hood.crypto_trading.schema.trading

hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.schema.trading.Errors(
        type="validation_error",
        errors=[
            hood.crypto_trading.schema.trading.Error(
                detail="This order cannot be canceled.",
                attr="non_field_errors",
            ),
        ],
    ),
    response=requests.Response(),
    error=None,
)
```

</details>

# Disclaimers

The authors do not provide any guarantees pertaining to this software's fitness for use. You are responsible for 
evaluating the software and ensuring its proper functionality prior to use. For more information, please reference the 
[license](LICENSE).

You could lose money using this software. While the author seeks to ensure its proper function, the author does not
provide any guarantee that the software will function as expected.

Information contained within this document and its associated software do not provide legal, financial, or accounting
advice.
