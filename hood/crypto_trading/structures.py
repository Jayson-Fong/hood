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


_T = TypeVar("_T", bound="DataclassInstance")


@dataclass(frozen=True, slots=True, kw_only=True)
class APIResponse(Generic[_T]):
    data: Optional[_T] = None
    response: Optional["requests.Response"] = None
    error: Optional[BaseException] = None


MaybeAPIResponse = APIResponse[Union[_T, "_schema.Errors"]]


__all__ = ["APIResponse", "MaybeAPIResponse", "QueryParams"]
