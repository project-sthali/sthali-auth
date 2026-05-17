"""SQLAlchemy ORM models for users and roles."""

from sqlalchemy import UUID, Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from sthali_db import BaseModel

user_roles = Table(
    "user_roles",
    BaseModel.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("role_id", UUID, ForeignKey("roles.id"), primary_key=True),
)


class UserModel(BaseModel):
    """ORM model representing an application user."""

    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String)

    roles = relationship("RoleModel", secondary=user_roles, back_populates="users")


class RoleModel(BaseModel):
    """ORM model representing a user role."""

    __tablename__ = "roles"

    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("UserModel", secondary=user_roles, back_populates="roles")
