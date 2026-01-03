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

While [Robinhood itself provides a sample client](https://docs.robinhood.com/crypto/trading/), it does not provide any
type hinting for its API's possible return types, types for order configuration, or methods to handle pagination.

The development of this package is **not affiliated with Robinhood**.

# Installation

The latest development release is installable from GitHub:

```shell
python3 -m pip install git+https://github.com/Jayson-Fong/hood
```

# Disclaimers

The authors do not provide any guarantees pertaining to this software's fitness for use. You are responsible for 
evaluating the software and ensuring its proper functionality prior to use. For more information, please reference the 
[license](LICENSE).

You could lose money using this software. While the author seeks to ensure its proper function, the author does not
provide any guarantee that the software will function as expected.

Information contained within this document and its associated software do not provide legal, financial, or accounting
advice.

# Backlog

- [ ] Endpoints
  - [X] Account
    - [X] Get Crypto Trading Account Details
  - [X] Market Data
    - [X] Get Best Price
    - [X] Get Estimated Price
  - [ ] Trading
    - [ ] Get Crypto Trading Pairs
    - [ ] Get Crypto Holdings
    - [ ] Get Crypto Orders
    - [ ] Place New Crypto Order
    - [ ] Cancel Open Crypto Order
- [ ] Command-Line Utilities
  - [ ] Key Generation
  - [ ] View Account Details
  - [ ] View Best Price
  - [ ] View Estimated Price
  - [ ] View Crypto Trading Pairs
  - [ ] View Crypto Holdings
  - [ ] Place New Crypto Order
  - [ ] Cancel Open Crypto Order
- [ ] API
  - Pagination Iterator
