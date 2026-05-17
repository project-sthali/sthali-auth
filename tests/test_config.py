"""Tests for sthali_auth.config."""
import unittest

from pydantic import ValidationError

from sthali_auth.config import ConfigSchema


class TestConfigSchema(unittest.TestCase):

    def test_empty_config_is_valid(self) -> None:
        result = ConfigSchema.model_validate({})
        self.assertIsNone(result.auth)

    def test_auth_none_by_default(self) -> None:
        result = ConfigSchema.model_validate({})
        self.assertIsNone(result.auth)

    def test_auth_api_key_accepted(self) -> None:
        data = {"auth": {"api_key": {"type": "header", "name": "x-api-key"}}}
        result = ConfigSchema.model_validate(data)
        self.assertIsNotNone(result.auth)
        self.assertIsNotNone(result.auth.api_key)  # type: ignore[union-attr]
        self.assertEqual(result.auth.api_key.name, "x-api-key")  # type: ignore[union-attr]

    def test_auth_api_key_type_stored(self) -> None:
        data = {"auth": {"api_key": {"type": "header", "name": "x-api-key"}}}
        result = ConfigSchema.model_validate(data)
        self.assertEqual(result.auth.api_key.type, "header")  # type: ignore[union-attr]

    def test_auth_api_key_optional_fields_default_none(self) -> None:
        data = {"auth": {"api_key": {"type": "cookie", "name": "session"}}}
        result = ConfigSchema.model_validate(data)
        api_key = result.auth.api_key  # type: ignore[union-attr]
        self.assertIsNone(api_key.scheme_name)
        self.assertIsNone(api_key.description)
        self.assertIsNone(api_key.auto_error)

    def test_auth_api_key_optional_fields_accepted(self) -> None:
        data = {
            "auth": {
                "api_key": {
                    "type": "header",
                    "name": "x-api-key",
                    "scheme_name": "ApiKey",
                    "description": "An API key",
                    "auto_error": False,
                }
            }
        }
        result = ConfigSchema.model_validate(data)
        api_key = result.auth.api_key  # type: ignore[union-attr]
        self.assertEqual(api_key.scheme_name, "ApiKey")
        self.assertFalse(api_key.auto_error)

    def test_auth_api_key_missing_name_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConfigSchema.model_validate({"auth": {"api_key": {"type": "header"}}})

    def test_auth_oauth2_accepted(self) -> None:
        data = {"auth": {"oauth2": {"access_token_expire_minutes": 30}}}
        result = ConfigSchema.model_validate(data)
        self.assertIsNotNone(result.auth)
        self.assertEqual(result.auth.oauth2.access_token_expire_minutes, 30)  # type: ignore[union-attr]

    def test_auth_oauth2_none_by_default(self) -> None:
        data = {"auth": {"api_key": {"type": "header", "name": "k"}}}
        result = ConfigSchema.model_validate(data)
        self.assertIsNone(result.auth.oauth2)  # type: ignore[union-attr]


if __name__ == "__main__":
    unittest.main()
