"""Tests for sthali_auth.dependencies.http."""
import unittest

from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, HTTPBearer

from sthali_auth.dependencies.http import HTTP, Types


class TestHTTPTypes(unittest.TestCase):

    def test_types_has_http_basic(self) -> None:
        self.assertEqual(Types.http_basic.value, "http_basic")

    def test_types_has_http_bearer(self) -> None:
        self.assertEqual(Types.http_bearer.value, "http_bearer")


class TestHTTP(unittest.TestCase):

    def test_http_basic_sets_http_basic_dependency(self) -> None:
        instance = HTTP(Types.http_basic)
        self.assertIsInstance(instance._dependency, HTTPBasic)

    def test_http_bearer_sets_http_bearer_dependency(self) -> None:
        instance = HTTP(Types.http_bearer)
        self.assertIsInstance(instance._dependency, HTTPBearer)

    def test_http_basic_annotation_type_is_http_basic_credentials(self) -> None:
        instance = HTTP(Types.http_basic)
        self.assertIs(instance._annotation_type, HTTPBasicCredentials)

    def test_http_bearer_annotation_type_is_http_authorization_credentials(self) -> None:
        instance = HTTP(Types.http_bearer)
        self.assertIs(instance._annotation_type, HTTPAuthorizationCredentials)

    def test_from_type_creates_instance(self) -> None:
        instance = HTTP.from_type("http_basic")
        self.assertIsInstance(instance, HTTP)

    def test_from_type_converts_string_to_enum(self) -> None:
        instance = HTTP.from_type("http_bearer")
        self.assertIsInstance(instance._dependency, HTTPBearer)

    def test_dependency_property_returns_annotated_type(self) -> None:
        instance = HTTP(Types.http_basic)
        dep = instance.dependency
        self.assertIsNotNone(dep)


if __name__ == "__main__":
    unittest.main()
