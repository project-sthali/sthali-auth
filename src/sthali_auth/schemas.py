"""Pydantic schemas for API request/response models.

This module provides base schemas with form field generation and HATEOAS support.
"""

from uuid import UUID

from sthali_db import BaseSchema


class RoleCreateSchema(BaseSchema):
    """Schema for creating a new role."""

    class Config:
        """{...}."""

        title = "Role"

    name: str


class RoleUpdateSchema(RoleCreateSchema):
    """{...}."""


class RoleReadSchema(RoleCreateSchema):
    """Schema for reading role data with ID."""

    id: UUID


RoleSchemas = (RoleCreateSchema, RoleReadSchema, RoleUpdateSchema)


class UserCreateSchema(BaseSchema):
    """Schema for creating a new user."""

    class Config:
        """{...}."""

        title = "User"

    name: str


class UserUpdateSchema(UserCreateSchema):
    """{...}."""


class UserReadSchema(UserCreateSchema):
    """Schema for reading user data with ID."""

    id: UUID


UserSchemas = (UserCreateSchema, UserReadSchema, UserUpdateSchema)
