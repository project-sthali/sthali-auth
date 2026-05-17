"""Pydantic schemas for User and Role resources."""

from typing import ClassVar
from uuid import UUID

from pydantic import ConfigDict
from sthali_db import BaseSchema


class RoleCreateSchema(BaseSchema):
    """Schema for creating a new role."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True, title="Role")

    name: str


class RoleUpdateSchema(RoleCreateSchema):
    """Schema for updating an existing role."""


class RoleReadSchema(RoleCreateSchema):
    """Schema for reading role data including the assigned ID."""

    id: UUID


RoleSchemas: tuple[type[RoleCreateSchema], type[RoleReadSchema], type[RoleUpdateSchema]] = (
    RoleCreateSchema,
    RoleReadSchema,
    RoleUpdateSchema,
)


class UserCreateSchema(BaseSchema):
    """Schema for creating a new user."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True, title="User")

    name: str


class UserUpdateSchema(UserCreateSchema):
    """Schema for updating an existing user."""


class UserReadSchema(UserCreateSchema):
    """Schema for reading user data including the assigned ID."""

    id: UUID


UserSchemas: tuple[type[UserCreateSchema], type[UserReadSchema], type[UserUpdateSchema]] = (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)
