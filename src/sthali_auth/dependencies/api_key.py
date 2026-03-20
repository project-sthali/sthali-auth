"""{...}."""
from enum import Enum

from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery

from . import Base


class Types(Enum):
    """{...}."""
    cookie = "cookie"
    header = "header"
    query = "query"


class APIKey(Base):
    """{...}."""
    _annotation_type = str

    def __init__(
        self,
        _type: Types,
        name: str,
        scheme_name: str | None = None,
        description: str | None = None,
        auto_error: bool | None = None,
    ):
        """{...}."""
        match _type:
            case "cookie":
                dependency_type = APIKeyCookie

            case "header":
                dependency_type = APIKeyHeader

            case "query":
                dependency_type = APIKeyQuery
            case _:
                raise NotImplementedError

        auto_error = auto_error if auto_error is not None else True
        self._dependency = dependency_type(
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )
