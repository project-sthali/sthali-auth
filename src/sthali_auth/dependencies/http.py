"""{...}."""
from enum import Enum

from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, HTTPBearer

from . import Base


class Types(Enum):
    """{...}."""
    http_basic = "http_basic"
    http_bearer = "http_bearer"


class HTTP(Base):
    """{...}."""

    def __init__(self, type: Types):
        """{...}."""
        match type:
            case "http_basic":
                scheme_type = HTTPBasic
                annotation_type = HTTPBasicCredentials
            case "http_bearer":
                scheme_type = HTTPBearer
                annotation_type = HTTPAuthorizationCredentials
            case _:
                raise NotImplementedError

        self._dependency = scheme_type()
        self._annotation_type = annotation_type
