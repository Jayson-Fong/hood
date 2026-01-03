import base64
from dataclasses import dataclass, InitVar, field
from typing import Union

from nacl.signing import SigningKey


from . import constants as _constants


@dataclass()
class Credential:

    api_key: str = field(repr=False)
    private_key_seed: InitVar[Union[bytes, SigningKey]]
    private_key: SigningKey = field(init=False, repr=False)

    def sign_message(
        self, path: str, body: str, timestamp: int, method: _constants.RequestMethod
    ) -> str:
        if not path.startswith("/"):
            path = f"/{path}"

        message = f"{self.api_key}{timestamp}{path}{method.name}{body}"
        signed_message = self.private_key.sign(message.encode("utf-8"))

        return base64.b64encode(signed_message.signature).decode("utf-8")

    @staticmethod
    def generate():
        return SigningKey.generate()

    def __post_init__(self, private_key_seed: Union[bytes, SigningKey]):
        if isinstance(private_key_seed, bytes):
            self.private_key = SigningKey(private_key_seed)
        else:
            self.private_key = private_key_seed


__all__ = ["Credential"]
