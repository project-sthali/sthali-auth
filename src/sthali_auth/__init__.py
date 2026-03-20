"""{...}."""

from enum import Enum
from typing import Any

from sthali_db import definitions_type

from .config import ConfigSchema
from .dependencies.api_key import APIKey
from .dependencies.http import HTTP
from .models import RoleModel, UserModel
from .schemas import (
    RoleCreateSchema,
    RoleReadSchema,
    RoleUpdateSchema,
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)

__all__ = [
    "APIKey",
    "ConfigSchema",
    "SthaliAuth",
    "definitions",
]

definitions: definitions_type = [
    (UserModel, (UserCreateSchema, UserReadSchema, UserUpdateSchema)),
    (RoleModel, (RoleCreateSchema, RoleReadSchema, RoleUpdateSchema)),
]


class Types(Enum):
    api_key = "api_key"
    http = "http"


class SthaliAuth:
    """{...}."""

    def __init__(self, _type: Types, definition: dict[str, Any]) -> None:
        """{...}."""
        match _type:
            case "api_key":
                dependency_module = APIKey
            case "http":
                dependency_module = HTTP
            case _:
                raise NotImplementedError

        self.client = dependency_module.from_type(**definition)

    @classmethod
    def from_type(cls, _type: Types, definition: dict[str, Any]) -> "SthaliAuth":
        """{...}."""
        return cls(_type, definition)
