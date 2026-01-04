from dataclasses import dataclass
from typing import (
    Union,
    List,
    Dict,
    Generic,
    TypeVar,
    TYPE_CHECKING,
    Optional,
    TypedDict,
)

if TYPE_CHECKING:
    import requests

QueryParams = Dict[str, Union[str, int, float, List[Union[str, int, float]]]]


T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class APIResponse(Generic[T]):
    data: Optional[T] = None
    response: Optional["requests.Response"] = None
    error: Optional[BaseException] = None


class ClientOptions(TypedDict):
    headers: Optional[Dict[str, str]]
    timeout: float


__all__ = ["QueryParams", "APIResponse"]
