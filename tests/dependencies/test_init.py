"""Tests for sthali_auth.dependencies."""
import unittest
from typing import Any
from unittest.mock import patch

from fastapi import Depends

from sthali_auth.dependencies import Base


class ConcreteBase(Base):

    def __init__(self, _type: str, *_args: Any, **_kwargs: Any) -> None:
        self._annotation_type = str
        self._dependency = lambda: "key"


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.instance = ConcreteBase("header")

    def test_from_type_returns_instance(self) -> None:
        result = ConcreteBase.from_type("header")
        self.assertIsInstance(result, ConcreteBase)

    def test_from_type_passes_type_to_init(self) -> None:
        with patch.object(ConcreteBase, "__init__", return_value=None) as mock_init:
            ConcreteBase.from_type("cookie", name="x-api-key")
        mock_init.assert_called_once_with("cookie", name="x-api-key")

    def test_from_type_returns_same_subclass(self) -> None:
        result = ConcreteBase.from_type("header")
        self.assertIsInstance(result, ConcreteBase)

    def test_dependency_contains_depends(self) -> None:
        dep = self.instance.dependency
        metadata = getattr(dep, "__metadata__", ())
        self.assertTrue(any(isinstance(m, type(Depends(lambda: None))) for m in metadata))

    def test_base_init_raises_not_implemented(self) -> None:
        bare = Base.__new__(Base)
        with self.assertRaises(NotImplementedError):
            Base.__init__(bare, "header")

    def test_dependency_property_is_not_none(self) -> None:
        dep = self.instance.dependency
        self.assertIsNotNone(dep)


if __name__ == "__main__":
    unittest.main()
