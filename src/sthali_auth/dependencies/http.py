"""HTTP authentication dependency (Basic or Bearer)."""

from enum import Enum
from typing import Any, Self

from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, HTTPBearer

from . import Base


class Types(Enum):
    """Supported HTTP authentication schemes."""

    http_basic = "http_basic"
    http_bearer = "http_bearer"


class HTTP(Base):
    """FastAPI dependency adapter for HTTP Basic / Bearer authentication."""

    @classmethod
    def from_type(cls, _type: str, **kwargs: Any) -> Self:
        """Instantiate an ``HTTP`` dependency by type string.

        Args:
            _type: One of ``"http_basic"`` or ``"http_bearer"``.
            **kwargs: Additional keyword arguments forwarded to ``__init__``.

        Returns:
            A new ``HTTP`` instance.
        """
        return cls(Types(_type), **kwargs)

    def __init__(self, _type: Types) -> None:
        """Initialise the HTTP authentication dependency.

        Args:
            _type: The HTTP authentication scheme to use.

        Raises:
            NotImplementedError: When ``_type`` is not a recognised ``Types`` member.
        """
        match _type:
            case Types.http_basic:
                scheme_type = HTTPBasic
                annotation_type = HTTPBasicCredentials
            case Types.http_bearer:
                scheme_type = HTTPBearer
                annotation_type = HTTPAuthorizationCredentials
            case _:
                raise NotImplementedError

        self._dependency = scheme_type()
        self._annotation_type = annotation_type
