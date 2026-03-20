"""{...}."""

from sthali_core.config import ConfigSchema as BaseConfigSchema


class ConfigSchema(BaseConfigSchema):
    """{...}."""

    class AuthSchema(BaseConfigSchema):
        """{...}."""

        class APIKeySchema(BaseConfigSchema):
            type: str
            name: str
            scheme_name: str | None = None
            description: str | None = None
            auto_error: bool | None = None

        class OAuth2Schema(BaseConfigSchema):
            access_token_expire_minutes: int

        api_key: APIKeySchema | None = None
        oauth2: OAuth2Schema | None = None

    auth: AuthSchema | None = None
