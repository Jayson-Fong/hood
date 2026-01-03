from . import _util
from ..crypto_trading import CryptoTradingClient


def accounts():
    credential = _util.get_credential()
    client = CryptoTradingClient(credential)

    result, err = client.accounts(create_namespace=True)
    print(result)
