import dataclasses
import inspect
from dataclasses import fields
from typing import Type, Optional, get_args, get_origin, Union

import requests

from .. import schema as _schema


def unpack_union(field_type: Type) -> Type:
    if get_origin(field_type) is Union:
        return get_args(field_type)[0]

    return field_type


def dataclass_pack(json_data, schema):
    if isinstance(json_data, dict):
        prepared_data = {}
        for field in fields(schema):
            if field.name not in json_data:
                continue

            field_type = unpack_union(field.type)
            origin = get_origin(field_type)

            if origin is list:
                prepared_data[field.name] = dataclass_pack(json_data[field.name], get_args(field_type)[0])
                continue

            if dataclasses.is_dataclass(field_type):
                prepared_data[field.name] = dataclass_pack(json_data[field.name], field_type)
                continue

            prepared_data[field.name] = json_data[field.name]

        return schema(**prepared_data)

    return None


def parse_response(response: requests.Response, schema: Optional[Type] = None):
    if not schema:
        return _schema.Message(body=response.text)

    try:
        json_data = response.json()
    except requests.RequestException:
        return None

    try:
        return dataclass_pack(json_data, schema)
    except Exception:
        return None
