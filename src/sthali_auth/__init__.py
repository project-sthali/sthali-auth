"""SthaliAuth factory and auth type definitions."""

from enum import Enum
from typing import Any, Self

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
    """Supported top-level authentication mechanisms."""

    api_key = "api_key"
    http = "http"


class SthaliAuth:
    """Factory for creating authentication dependency clients.

    Attributes:
        client: The instantiated authentication dependency.
    """

    def __init__(self, _type: Types, definition: dict[str, Any]) -> None:
        """Instantiate the correct authentication dependency.

        Args:
            _type: The authentication mechanism to use.
            definition: Keyword arguments forwarded to the dependency's ``from_type``.

        Raises:
            NotImplementedError: When ``_type`` is not a recognised value.
        """
        dependency_module: type[APIKey | HTTP]
        match _type:
            case Types.api_key:
                dependency_module = APIKey
            case Types.http:
                dependency_module = HTTP
            case _:
                raise NotImplementedError

        self.client = dependency_module.from_type(**definition)

    @classmethod
    def from_type(cls, _type: Types, definition: dict[str, Any]) -> Self:
        """Create a ``SthaliAuth`` instance from a type enum and definition dict.

        Args:
            _type: The authentication mechanism to use.
            definition: Keyword arguments forwarded to the dependency's ``from_type``.

        Returns:
            A new ``SthaliAuth`` instance.
        """
        return cls(_type, definition)
