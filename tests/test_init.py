"""Tests for sthali_auth."""
import unittest

from sthali_auth import SthaliAuth, Types, definitions
from sthali_auth.dependencies.api_key import APIKey
from sthali_auth.dependencies.http import HTTP
from sthali_auth.models import RoleModel, UserModel


class TestDefinitions(unittest.TestCase):

    def test_definitions_is_a_list(self) -> None:
        self.assertIsInstance(definitions, list)

    def test_definitions_has_two_entries(self) -> None:
        self.assertEqual(len(definitions), 2)

    def test_definitions_first_entry_is_user_model(self) -> None:
        model, _ = definitions[0]
        self.assertIs(model, UserModel)

    def test_definitions_second_entry_is_role_model(self) -> None:
        model, _ = definitions[1]
        self.assertIs(model, RoleModel)

    def test_definitions_each_entry_has_three_schemas(self) -> None:
        for _, schemas in definitions:
            self.assertEqual(len(schemas), 3)


class TestSthaliAuthTypes(unittest.TestCase):

    def test_types_has_api_key(self) -> None:
        self.assertEqual(Types.api_key.value, "api_key")

    def test_types_has_http(self) -> None:
        self.assertEqual(Types.http.value, "http")


class TestSthaliAuth(unittest.TestCase):

    def _make_api_key_instance(self) -> SthaliAuth:
        definition = {"_type": "header", "name": "x-api-key"}
        return SthaliAuth(Types.api_key, definition)

    def _make_http_instance(self) -> SthaliAuth:
        definition = {"_type": "http_basic"}
        return SthaliAuth(Types.http, definition)

    def test_api_key_type_sets_api_key_client(self) -> None:
        auth = self._make_api_key_instance()
        self.assertIsInstance(auth.client, APIKey)

    def test_http_type_sets_http_client(self) -> None:
        auth = self._make_http_instance()
        self.assertIsInstance(auth.client, HTTP)

    def test_from_type_returns_sthali_auth_instance(self) -> None:
        result = SthaliAuth.from_type(Types.api_key, {"_type": "header", "name": "k"})
        self.assertIsInstance(result, SthaliAuth)

    def test_from_type_stores_client(self) -> None:
        result = SthaliAuth.from_type(Types.http, {"_type": "http_basic"})
        self.assertIsNotNone(result.client)

    def test_from_type_produces_same_result_as_init(self) -> None:
        definition = {"_type": "header", "name": "x-key"}
        direct = SthaliAuth(Types.api_key, definition)
        via_factory = SthaliAuth.from_type(Types.api_key, definition)
        self.assertIsInstance(direct.client, type(via_factory.client))

    def test_client_is_set_after_init(self) -> None:
        auth = self._make_api_key_instance()
        self.assertIsNotNone(auth.client)


if __name__ == "__main__":
    unittest.main()
