from typing import TypeVar, Union, Tuple, Protocol, List, Dict

QueryParams = Dict[str, Union[str, List[str]]]


class ErrorResponseEntry(Protocol):
    detail: str
    attr: str


class ErrorResponse(Protocol):
    type: str
    errors: List[ErrorResponseEntry]


T = TypeVar("T")


class ResultsResponse(Protocol[T]):
    results: List[T]


class ResultPageResponse(Protocol[T]):
    next: str
    previous: str
    results: List[T]


APIResponse = Union[Tuple[T, None], Tuple[None, Exception]]
MaybeAPIResponse = Union[APIResponse[T], APIResponse[ErrorResponse]]


__all__ = [
    "APIResponse",
    "MaybeAPIResponse",
    "ErrorResponseEntry",
    "ErrorResponse",
    "ResultsResponse",
    "ResultPageResponse",
]
