import base64
import logging
from dataclasses import dataclass, InitVar, field
from typing import Union

import nacl.signing


from . import constants as _constants


_logger = logging.getLogger(__package__)


@dataclass(slots=True)
class Credential:

    api_key: str = field(repr=False)
    private_key_seed: InitVar[Union[bytes, nacl.signing.SigningKey]]
    private_key: nacl.signing.SigningKey = field(init=False, repr=False)

    def sign_message(
        self, path: str, body: str, timestamp: int, method: _constants.RequestMethod
    ) -> str:
        """
        Create a Base64-encoded signature for an API request.

        Args:
            path: The request path.
            body: Request body included in the signed message.
            timestamp: Timestamp included in the signed message.
            method: HTTP method enum whose `name` is included in the signed message.

        Returns:
            Base64-encoded signature.
        """

        if not path.startswith("/"):
            path = f"/{path}"

        _logger.debug(
            "Signing request: Timestamp %s - Path %s - Method %s",
            timestamp,
            path,
            method.name,
        )
        message = f"{self.api_key}{timestamp}{path}{method.name}{body}"
        signed_message = self.private_key.sign(message.encode("utf-8"))

        return base64.b64encode(signed_message.signature).decode("utf-8")

    @staticmethod
    def generate() -> nacl.signing.SigningKey:
        """
        Create a new Ed25519 private signing key.

        Returns:
            nacl.signing.SigningKey: A newly generated Ed25519 private key for signing.
        """

        return nacl.signing.SigningKey.generate()

    def __post_init__(
        self, private_key_seed: Union[bytes, nacl.signing.SigningKey]
    ) -> None:
        """
        Initialize the instance's `private_key` from the provided seed.

        Args:
            private_key_seed: A 32-byte seed or `SigningKey` instance.
        """

        if isinstance(private_key_seed, bytes):
            self.private_key = nacl.signing.SigningKey(private_key_seed)
        else:
            self.private_key = private_key_seed


__all__ = ["Credential"]
