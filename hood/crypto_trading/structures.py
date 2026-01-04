from dataclasses import dataclass
from typing import (
    Union,
    List,
    Dict,
    Generic,
    TypeVar,
    TYPE_CHECKING,
    Optional,
)

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from _typeshed import DataclassInstance

    import requests
    # noinspection PyUnresolvedReferences
    from .. import schema as _schema

QueryParams = Dict[str, Union[str, int, float, List[Union[str, int, float]]]]


T = TypeVar("T", bound="DataclassInstance")


@dataclass(frozen=True, slots=True, kw_only=True)
class APIResponse(Generic[T]):
    data: Optional[T] = None
    response: Optional["requests.Response"] = None
    error: Optional[BaseException] = None


MaybeAPIResponse = APIResponse[Union[T, "_schema.Errors"]]


__all__ = ["APIResponse", "MaybeAPIResponse", "QueryParams"]
