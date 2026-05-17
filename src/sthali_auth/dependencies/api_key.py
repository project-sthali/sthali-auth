"""API-key authentication dependency (cookie, header, or query parameter)."""

from enum import Enum
from typing import Any, ClassVar, Self

from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery

from . import Base


class Types(Enum):
    """Supported API-key transport mechanisms."""

    cookie = "cookie"
    header = "header"
    query = "query"


class APIKey(Base):
    """FastAPI dependency adapter for API-key authentication.

    Attributes:
        _annotation_type: Always ``str`` — the extracted key value type.
    """

    _annotation_type: ClassVar[type[str]] = str

    @classmethod
    def from_type(cls, _type: str, **kwargs: Any) -> Self:
        """Instantiate an ``APIKey`` dependency by type string.

        Args:
            _type: One of ``"cookie"``, ``"header"``, or ``"query"``.
            **kwargs: Additional keyword arguments forwarded to ``__init__``.

        Returns:
            A new ``APIKey`` instance.
        """
        return cls(Types(_type), **kwargs)

    def __init__(
        self,
        _type: Types,
        name: str,
        scheme_name: str | None = None,
        description: str | None = None,
        auto_error: bool | None = None,  # noqa: FBT001
    ) -> None:
        """Initialise the API-key dependency for the requested transport.

        Args:
            _type: Whether to extract the key from a cookie, header, or query param.
            name: The cookie / header / query-parameter name.
            scheme_name: Optional OpenAPI security scheme name.
            description: Optional OpenAPI description.
            auto_error: Raise HTTP 403 automatically when the key is absent.
                Defaults to ``True`` when ``None``.

        Raises:
            NotImplementedError: When ``_type`` is not a recognised ``Types`` member.
        """
        dependency_type: type[APIKeyCookie | APIKeyHeader | APIKeyQuery]
        match _type:
            case Types.cookie:
                dependency_type = APIKeyCookie
            case Types.header:
                dependency_type = APIKeyHeader
            case Types.query:
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
