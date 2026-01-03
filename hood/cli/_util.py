import base64
import pathlib
import sys
from typing import Optional

from nacl.signing import SigningKey

from ..crypto_trading import auth as _auth


CONFIG_PATH = pathlib.Path.home() / ".config" / ".hood"
API_KEY_PATH = CONFIG_PATH / "api_key"
PRIVATE_KEY_PATH = CONFIG_PATH / "private_key"


def handle_exception(message: str, *handle: type[BaseException]):
    if not handle:
        handle = (Exception,)

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except handle as err:
                sys.exit(f"{message}: {err}")

        return wrapper

    return decorator


@handle_exception("Failed to read API key from disk")
def get_api_key(force: bool = True) -> Optional[str]:
    if not API_KEY_PATH.is_file():
        if force:
            sys.exit("An API key is required.")

        return None

    return API_KEY_PATH.read_text().strip()


@handle_exception("Failed to write API key to disk")
def write_api_key(key: str):
    API_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    API_KEY_PATH.write_text(key)


@handle_exception("Failed to read private key from disk")
def get_private_key(force: bool = True) -> Optional[SigningKey]:
    if not PRIVATE_KEY_PATH.is_file():
        if force:
            sys.exit("An API key is required.")

        return None

    return SigningKey(base64.b64decode(PRIVATE_KEY_PATH.read_text().strip()))


@handle_exception("Failed to write private key to disk")
def write_private_key(key: SigningKey):
    key_b64 = base64.b64encode(key.encode()).decode()

    PRIVATE_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRIVATE_KEY_PATH.write_text(key_b64)


def get_credential():
    return _auth.Credential(get_api_key(), get_private_key().encode())
