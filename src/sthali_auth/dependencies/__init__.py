"""{...}."""
from typing import Annotated, Any

from fastapi import Depends


class Base:
    """{...}."""

    _annotation_type: Any
    _dependency: Any

    def __init__(self, _type: str, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_type(cls, _type: str, **kwargs) -> "Base":
        """{...}."""
        return cls(_type, **kwargs)

    @property
    def dependency(self):
        """{...}."""
        return Annotated[self._annotation_type, Depends(self._dependency)]
