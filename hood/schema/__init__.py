from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(frozen=True, slots=True, kw_only=True)
class Message:
    body: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Error:
    detail: Optional[str] = None
    attr: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Errors:
    type: Optional[str] = None
    errors: List[Error] = field(default_factory=list)


__all__ = ["Message", "Error", "Errors"]
