import pydantic
import sqlmodel


class User(sqlmodel.SQLModel):
    email: pydantic.EmailStr = sqlmodel.Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = sqlmodel.Field(default=None, max_length=255)
    password: str = sqlmodel.Field(min_length=8, max_length=128)
