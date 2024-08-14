"""This module provides the dependencies for sthali-auth usage."""
from .clients.api_key import APIKey, APIKeyAuth

api_key = APIKey("api_key")
api_key_auth = APIKeyAuth(api_key, "header", "service")

api_key_auth_dependency = api_key_auth.dependency
