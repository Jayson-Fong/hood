from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Message:
    body: Optional[str] = None


@dataclass
class Error:
    detail: Optional[str] = None
    attr: Optional[str] = None


@dataclass
class Errors:
    type: Optional[str] = None
    errors: List[Error] = field(default_factory=list)


__all__ = ["Message", "Error", "Errors"]
