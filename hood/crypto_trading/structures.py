from typing import TypeVar, Union, Tuple, Protocol, List, Dict, TypedDict, Optional

QueryParams = Dict[str, Union[str, List[str]]]


# pylint: disable=too-few-public-methods
class ErrorResponseEntryProtocol(Protocol):
    detail: str
    attr: str


class ErrorResponseEntryDict(TypedDict):
    detail: str
    attr: str


# pylint: disable=too-few-public-methods
class ErrorResponseProtocol(Protocol):
    type: str
    errors: List[ErrorResponseEntryProtocol]


class ErrorResponseDict(TypedDict):
    type: str
    errors: List[ErrorResponseEntryDict]


T = TypeVar("T")

# This would be more accurately expressed as: `Union[Tuple[T], None], Tuple[None, Exception]`
# However, it seems some IDEs won't type hint properly in this case. Hence, `Optional` is
# leveraged. This type hint is not exact as it implies we could get both a response and an
# exception or not have either, which should not occur.
APIResponse = Tuple[Optional[T], Optional[Exception]]
MaybeAPIResponseProtocol = APIResponse[Union[T, ErrorResponseProtocol]]
MaybeAPIResponseDict = APIResponse[Union[T, ErrorResponseDict]]

# This may seem a bit redundant compared to:
#   `Union[MaybeAPIResponseProtocol[T], MaybeAPIResponseDict[T]]`
# However, it is defined in this manner to help type hinting within IDEs.
MaybeAPIResponse = APIResponse[
    Union[T, Union[ErrorResponseProtocol, ErrorResponseDict]]
]

__all__ = [
    "APIResponse",
    "MaybeAPIResponseProtocol",
    "MaybeAPIResponseDict",
]
