from dataclasses import dataclass, field
from typing import Optional, List, Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class Message:
    body: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Error:
    detail: Optional[str] = None
    attr: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Errors:
    """
    Contains a list of errors returned by the API.

    Attributes:
        type: The type of error.
            "validation_error" for status code 400.
            "client_error" for all 4xx status codes except 400.
            "server_error" for all 5xx status codes.
    """

    type: Optional[Literal["validation_error", "client_error", "server_error"]] = None
    errors: List[Error] = field(default_factory=list)


__all__ = ["Error", "Errors", "Message"]
