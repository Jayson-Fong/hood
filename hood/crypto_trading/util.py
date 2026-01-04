import datetime
from typing import Optional, cast
from urllib.parse import urlparse, urlencode, parse_qs

from . import structures as _struct
from .structures import QueryParams


def get_current_timestamp() -> int:
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


def inject_qs(url: str, params: Optional[_struct.QueryParams] = None) -> str:
    if not params:
        return url

    parsed_url = urlparse(url)
    query_params = cast(QueryParams, parse_qs(parsed_url.query))
    query_params.update(params)

    updated_qs = urlencode(query_params, doseq=True)
    return parsed_url._replace(query=updated_qs).geturl()


__all__ = ["get_current_timestamp", "inject_qs"]
