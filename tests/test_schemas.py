"""Tests for sthali_auth.schemas."""
import unittest
from uuid import UUID

from pydantic import ValidationError

from sthali_auth.schemas import (
    RoleCreateSchema,
    RoleReadSchema,
    RoleSchemas,
    RoleUpdateSchema,
    UserCreateSchema,
    UserReadSchema,
    UserSchemas,
    UserUpdateSchema,
)


class TestRoleSchemas(unittest.TestCase):

    def test_role_create_schema_accepts_name(self) -> None:
        result = RoleCreateSchema.model_validate({"name": "admin"})
        self.assertEqual(result.name, "admin")

    def test_role_create_schema_missing_name_raises(self) -> None:
        with self.assertRaises(ValidationError):
            RoleCreateSchema.model_validate({})

    def test_role_read_schema_requires_id(self) -> None:
        with self.assertRaises(ValidationError):
            RoleReadSchema.model_validate({"name": "admin"})

    def test_role_read_schema_accepts_valid_uuid(self) -> None:
        uid = "12345678-1234-5678-1234-567812345678"
        result = RoleReadSchema.model_validate({"name": "admin", "id": uid})
        self.assertIsInstance(result.id, UUID)

    def test_role_update_schema_accepts_name(self) -> None:
        result = RoleUpdateSchema.model_validate({"name": "editor"})
        self.assertEqual(result.name, "editor")

    def test_role_schemas_tuple_has_three_elements(self) -> None:
        self.assertEqual(len(RoleSchemas), 3)

    def test_role_schemas_tuple_first_is_create(self) -> None:
        self.assertIs(RoleSchemas[0], RoleCreateSchema)

    def test_role_schemas_tuple_second_is_read(self) -> None:
        self.assertIs(RoleSchemas[1], RoleReadSchema)

    def test_role_schemas_tuple_third_is_update(self) -> None:
        self.assertIs(RoleSchemas[2], RoleUpdateSchema)

    def test_role_create_schema_from_attributes(self) -> None:
        class _FakeRow:
            name = "viewer"

        result = RoleCreateSchema.model_validate(_FakeRow(), from_attributes=True)
        self.assertEqual(result.name, "viewer")

    def test_role_schema_title(self) -> None:
        schema = RoleCreateSchema.model_json_schema()
        self.assertEqual(schema.get("title"), "Role")


class TestUserSchemas(unittest.TestCase):

    def test_user_create_schema_accepts_name(self) -> None:
        result = UserCreateSchema.model_validate({"name": "alice"})
        self.assertEqual(result.name, "alice")

    def test_user_create_schema_missing_name_raises(self) -> None:
        with self.assertRaises(ValidationError):
            UserCreateSchema.model_validate({})

    def test_user_read_schema_requires_id(self) -> None:
        with self.assertRaises(ValidationError):
            UserReadSchema.model_validate({"name": "alice"})

    def test_user_read_schema_accepts_valid_uuid(self) -> None:
        uid = "12345678-1234-5678-1234-567812345678"
        result = UserReadSchema.model_validate({"name": "alice", "id": uid})
        self.assertIsInstance(result.id, UUID)

    def test_user_update_schema_accepts_name(self) -> None:
        result = UserUpdateSchema.model_validate({"name": "bob"})
        self.assertEqual(result.name, "bob")

    def test_user_schemas_tuple_has_three_elements(self) -> None:
        self.assertEqual(len(UserSchemas), 3)

    def test_user_schemas_tuple_first_is_create(self) -> None:
        self.assertIs(UserSchemas[0], UserCreateSchema)

    def test_user_schemas_tuple_second_is_read(self) -> None:
        self.assertIs(UserSchemas[1], UserReadSchema)

    def test_user_schemas_tuple_third_is_update(self) -> None:
        self.assertIs(UserSchemas[2], UserUpdateSchema)

    def test_user_schema_title(self) -> None:
        schema = UserCreateSchema.model_json_schema()
        self.assertEqual(schema.get("title"), "User")


if __name__ == "__main__":
    unittest.main()
