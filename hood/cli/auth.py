import base64
import getpass

from . import _util
from ..crypto_trading import auth as _auth


def generate():
    # TODO: Check if already exists

    private_key = _auth.Credential.generate()
    public_key = base64.b64encode(private_key.verify_key.encode()).decode()

    print("Public Key:", public_key)
    api_key = getpass.getpass("Enter API Key: ")

    _util.write_api_key(api_key)
    _util.write_private_key(private_key)
