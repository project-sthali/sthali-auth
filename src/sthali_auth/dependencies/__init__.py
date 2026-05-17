"""Base class for FastAPI authentication dependency wrappers."""

from typing import Annotated, Any, Self

from fastapi import Depends


class Base:
    """Abstract base for authentication dependency adapters.

    Subclasses must set ``_annotation_type`` and populate ``_dependency``
    in ``__init__`` before the ``dependency`` property is accessed.

    Attributes:
        _annotation_type: The Python type injected by FastAPI for this dependency.
        _dependency: The FastAPI security callable used with ``Depends``.
    """

    _annotation_type: Any
    _dependency: Any

    def __init__(self, _type: str, *args: Any, **kwargs: Any) -> None:
        """Not directly instantiable — use ``from_type`` on a concrete subclass.

        Args:
            _type: The authentication sub-type string.
            *args: Forwarded positional arguments.
            **kwargs: Forwarded keyword arguments.

        Raises:
            NotImplementedError: Always; concrete subclasses must override.
        """
        raise NotImplementedError

    @classmethod
    def from_type(cls, _type: str, **kwargs: Any) -> Self:
        """Instantiate a concrete dependency by type string.

        Args:
            _type: The authentication sub-type string (e.g. ``"header"``).
            **kwargs: Additional keyword arguments forwarded to ``__init__``.

        Returns:
            A new instance of the concrete subclass.
        """
        return cls(_type, **kwargs)

    @property
    def dependency(self) -> Any:
        """Return the ``Annotated`` type for use as a FastAPI dependency.

        Returns:
            An ``Annotated`` type combining ``_annotation_type`` and ``Depends(_dependency)``.
        """
        return Annotated[self._annotation_type, Depends(self._dependency)]
