"""Configuration schemas for sthali-auth."""

from sthali_core.config import ConfigSchema as BaseConfigSchema


class ConfigSchema(BaseConfigSchema):
    """Top-level configuration schema extending the core config."""

    class AuthSchema(BaseConfigSchema):
        """Authentication configuration block."""

        class APIKeySchema(BaseConfigSchema):
            """API-key authentication parameters."""

            type: str
            name: str
            scheme_name: str | None = None
            description: str | None = None
            auto_error: bool | None = None

        class OAuth2Schema(BaseConfigSchema):
            """OAuth2 authentication parameters."""

            access_token_expire_minutes: int

        api_key: APIKeySchema | None = None
        oauth2: OAuth2Schema | None = None

    auth: AuthSchema | None = None
