"""Tests for sthali_auth.dependencies.api_key."""
import unittest

from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery

from sthali_auth.dependencies.api_key import APIKey, Types


class TestAPIKeyTypes(unittest.TestCase):

    def test_types_has_cookie(self) -> None:
        self.assertEqual(Types.cookie.value, "cookie")

    def test_types_has_header(self) -> None:
        self.assertEqual(Types.header.value, "header")

    def test_types_has_query(self) -> None:
        self.assertEqual(Types.query.value, "query")


class TestAPIKey(unittest.TestCase):

    def test_header_type_sets_api_key_header_dependency(self) -> None:
        instance = APIKey(Types.header, name="x-api-key")
        self.assertIsInstance(instance._dependency, APIKeyHeader)

    def test_cookie_type_sets_api_key_cookie_dependency(self) -> None:
        instance = APIKey(Types.cookie, name="session")
        self.assertIsInstance(instance._dependency, APIKeyCookie)

    def test_query_type_sets_api_key_query_dependency(self) -> None:
        instance = APIKey(Types.query, name="api_key")
        self.assertIsInstance(instance._dependency, APIKeyQuery)

    def test_annotation_type_is_str(self) -> None:
        instance = APIKey(Types.header, name="x-api-key")
        self.assertIs(instance._annotation_type, str)

    def test_auto_error_defaults_to_true_when_none(self) -> None:
        instance = APIKey(Types.header, name="x-api-key", auto_error=None)
        # FastAPI security classes store auto_error on the object
        self.assertTrue(instance._dependency.auto_error)

    def test_auto_error_false_is_passed_through(self) -> None:
        instance = APIKey(Types.header, name="x-api-key", auto_error=False)
        self.assertFalse(instance._dependency.auto_error)

    def test_name_is_stored_on_dependency(self) -> None:
        instance = APIKey(Types.header, name="my-key")
        self.assertEqual(instance._dependency.model.name, "my-key")

    def test_from_type_creates_instance(self) -> None:
        instance = APIKey.from_type("header", name="x-api-key")
        self.assertIsInstance(instance, APIKey)

    def test_from_type_converts_string_to_enum(self) -> None:
        instance = APIKey.from_type("cookie", name="session")
        self.assertIsInstance(instance._dependency, APIKeyCookie)

    def test_dependency_property_is_annotated_type(self) -> None:
        instance = APIKey(Types.header, name="x-api-key")
        dep = instance.dependency
        self.assertIsNotNone(dep)


if __name__ == "__main__":
    unittest.main()
