import datetime
from types import SimpleNamespace
from typing import Optional, Union, TypeVar, List, cast, Dict
from urllib.parse import urlparse, urlencode, parse_qs

from . import structures as _struct


def get_current_timestamp() -> int:
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


T = TypeVar("T")


def dict_to_namespace(d) -> Union[SimpleNamespace, List, T]:
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})

    if isinstance(d, list):
        return [dict_to_namespace(i) for i in d]

    return d


def inject_qs(url: str, params: Optional[_struct.QueryParams] = None) -> str:
    if not params:
        return url

    parsed_url = urlparse(url)
    query_params = cast(Dict[str, Union[str, List[str]]], parse_qs(parsed_url.query))
    query_params.update(params)

    updated_qs = urlencode(query_params, doseq=True)
    return parsed_url._replace(query=updated_qs).geturl()


__all__ = ["get_current_timestamp", "dict_to_namespace", "inject_qs"]
