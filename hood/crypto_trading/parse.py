import dataclasses
import decimal
from dataclasses import fields
from typing import (
    Type,
    Optional,
    get_args,
    get_origin,
    Union,
    Any,
    TYPE_CHECKING,
    TypeVar,
    cast,
)

import requests

from .. import schema as _schema


if TYPE_CHECKING:
    from _typeshed import DataclassInstance  # noqa


def unpack_union(field_type: Union[Type[Any], str]) -> Union[Type[Any], str]:
    if get_origin(field_type) is Union:
        return get_args(field_type)[0]

    return field_type


_T = TypeVar("_T", bound="DataclassInstance")


def dataclass_pack(json_data: Any, schema: Type[_T]) -> Optional[_T]:
    if isinstance(json_data, dict):
        prepared_data = {}
        for field in fields(schema):
            if field.name not in json_data:
                continue

            field_type = unpack_union(field.type)

            if isinstance(field_type, str):
                prepared_data[field.name] = json_data[field.name]
                continue

            origin = get_origin(field_type)

            if origin is list:
                prepared_data[field.name] = [
                    dataclass_pack(entry, get_args(field_type)[0])
                    for entry in json_data[field.name]
                ]
                continue

            if dataclasses.is_dataclass(field_type):
                prepared_data[field.name] = dataclass_pack(
                    json_data[field.name], field_type
                )
                continue

            if field_type in (int, float, decimal.Decimal):
                try:
                    prepared_data[field.name] = field_type(json_data[field.name])
                    continue
                except (ValueError, TypeError, decimal.InvalidOperation):
                    pass

            prepared_data[field.name] = json_data[field.name]

        return schema(**prepared_data)

    return None


def parse_response(
    response: requests.Response, schema: Optional[Type[_T]] = None
) -> Optional[_T]:
    if not schema:
        return None

    if schema is _schema.Message:
        return cast(_T, _schema.Message(body=response.text))

    try:
        json_data = response.json()
    except requests.RequestException:
        return None

    return dataclass_pack(json_data, schema)


__all__ = ["dataclass_pack", "parse_response"]
