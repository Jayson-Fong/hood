<!--suppress HtmlDeprecatedAttribute-->
<div align="center">
   <h1>🪶 hood</h1>

</div>

<hr />

<div align="center">

[💼 Purpose](#purpose) | [🛠️️ Installation](#installation) | [🛡️ Disclaimers](#disclaimers) | [📋 Backlog](#backlog)

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

```text
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

When using `hood`'s dedicated methods to make requests against Robinhood's Crypto Trading API, the function caller
will receive an instance of `hood.structures.APIResponse`, containing the following attributes:

- data (`None` or Dataclass Instance): Parsed response data.
- response (`None` or `requests.Response`): Response from the Crypto Trading API.
- error (`BaseException`): Exception if one was raised while processing the request.

### Account Endpoints

<details>
<summary>Get Crypto Trading Account Details</summary>

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.accounts()
```

```text
hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.account.TradingAccountDetail(
        account_number='000000000000',
        status='active',
        buying_power=decimal.Decimal('000.0000'),
        buying_power_currency='USD'
    ), 
    response=<requests.Response [200]>,
    error=None
)
```

</details>


### Market Data Endpoints

<details>
<summary>Get Best Price</summary>

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.best_bid_ask("BTC-USD", "ETH-USD")
```

```text
hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.market.BestBidAskResults(
        results=[
            hood.crypto_trading.market.BestBidAsk(
                symbol='BTC-USD',
                price=decimal.Decimal('94200.49475077'),
                bid_inclusive_of_sell_spread=decimal.Decimal('93401.43950154'),
                sell_spread=decimal.Decimal('0.0084825'),
                ask_inclusive_of_buy_spread=decimal.Decimal('94999.55'),
                buy_spread=decimal.Decimal('0.0084825'),
                timestamp='2026-01-05T21:04:16.35583523Z'
            ),
            hood.crypto_trading.market.BestBidAsk(
                symbol='ETH-USD',
                price=decimal.Decimal('3247.68922388'),
                bid_inclusive_of_sell_spread=decimal.Decimal('3220.746636'),
                sell_spread=decimal.Decimal('0.00829593'),
                ask_inclusive_of_buy_spread=decimal.Decimal('3274.63181176'),
                buy_spread=decimal.Decimal('0.00829593'),
                timestamp='2026-01-05T21:04:16.355835525Z'
            )
        ]
    ),
    response=<requests.Response [200]>,
    error=None
)
```

</details>

<details>
<summary>Get Estimated Price</summary>

```python
from hood.crypto_trading import CryptoTradingClient, auth

credential = auth.Credential("API_KEY_HERE", b"PRIVATE_KEY_HERE")
client = CryptoTradingClient(credential)
client.estimated_price("BTC-USD", "both", 0.1, "1")
```

```text
hood.crypto_trading.structures.APIResponse(
    data=hood.crypto_trading.market.MarketEstimateResults(
        results=[
            hood.crypto_trading.market.MarketEstimate(
                symbol='BTC-USD',
                side='bid',
                price=decimal.Decimal('94110.38097125'),
                quantity=decimal.Decimal('0.1'),
                bid_inclusive_of_sell_spread=decimal.Decimal('93311.1019425'),
                sell_spread=decimal.Decimal('0.008493'),
                ask_inclusive_of_buy_spread=None,
                buy_spread=None,
                timestamp='2026-01-05T16:08:10.270830931-05:00'
            ),
            hood.crypto_trading.market.MarketEstimate(
                symbol='BTC-USD',
                side='ask',
                price=decimal.Decimal('94110.38097125'),
                quantity=decimal.Decimal('0.1'),
                bid_inclusive_of_sell_spread=None,
                sell_spread=None,
                ask_inclusive_of_buy_spread=decimal.Decimal('94909.66'),
                buy_spread=decimal.Decimal('0.008493'),
                timestamp='2026-01-05T16:08:10.270830931-05:00'
            ),
            hood.crypto_trading.market.MarketEstimate(
                symbol='BTC-USD',
                side='bid',
                price=decimal.Decimal('94109.17804723'),
                quantity=decimal.Decimal('1'),
                bid_inclusive_of_sell_spread=decimal.Decimal('93307.82609446'),
                sell_spread=decimal.Decimal('0.00851513'),
                ask_inclusive_of_buy_spread=None,
                buy_spread=None,
                timestamp='2026-01-05T16:08:10.270830931-05:00'
            ),
            hood.crypto_trading.market.MarketEstimate(
                symbol='BTC-USD',
                side='ask',
                price=decimal.Decimal('94109.17804723'),
                quantity=decimal.Decimal('1'),
                bid_inclusive_of_sell_spread=None,
                sell_spread=None,
                ask_inclusive_of_buy_spread=decimal.Decimal('94910.53'),
                buy_spread=decimal.Decimal('0.00851513'),
                timestamp='2026-01-05T16:08:10.270830931-05:00'
            )
        ]
    ),
    response=<requests.Response [200]>,
    error=None
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

# Backlog

- [X] Endpoints
  - [X] Account
    - [X] Get Crypto Trading Account Details
  - [X] Market Data
    - [X] Get Best Price
    - [X] Get Estimated Price
  - [X] Trading
    - [X] Get Crypto Trading Pairs
    - [X] Get Crypto Holdings
    - [X] Get Crypto Orders
    - [X] Place New Crypto Order
    - [X] Cancel Open Crypto Order
- [ ] API
  - [ ] Pagination Iterator
