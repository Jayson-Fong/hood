import datetime
from typing import Optional, cast
from urllib.parse import urlparse, urlencode, parse_qs

from . import structures as _struct
from .structures import QueryParams


def get_current_timestamp() -> int:
    """
    Get the current UTC time as an integer UNIX timestamp (seconds since the epoch).

    Returns:
        Current UTC UNIX timestamp in seconds.
    """

    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


def inject_qs(url: str, params: Optional[_struct.QueryParams] = None) -> str:
    """
    Produce a URL with the given query parameters merged into its query string.

    Args:
        url: The original URL to update.
        params: Mapping of query parameter names to values. Values may be strings or lists of strings.

    Returns:
        str: The updated URL string with the merged query parameters encoded into its query component.
    """

    if not params:
        return url

    parsed_url = urlparse(url)
    query_params = cast(QueryParams, parse_qs(parsed_url.query))
    query_params.update(params)

    updated_qs = urlencode(query_params, doseq=True)
    return parsed_url._replace(query=updated_qs).geturl()


__all__ = ["inject_qs", "get_current_timestamp"]
