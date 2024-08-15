"""This module provides the dependencies for sthali-auth usage."""
from typing import Annotated, Literal

from fastapi import Depends, Request
from fastapi.routing import APIRoute
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery
from pydantic.dataclasses import dataclass

from . import ServiceClient


@dataclass
class APIKey:
    name: str
    scheme_name: str | None = None
    description: str | None = None
    auto_error: bool = True


@dataclass
class APIKeySpecification:
    type: Literal["header", "cookie", "query"]
    api_key: APIKey


class APIKeyAuth:
    client = ServiceClient()

    def __init__(self, api_key_spec: APIKeySpecification, service: str) -> None:
        if api_key_spec.type == "header":
            scheme = APIKeyHeader
        elif api_key_spec.type == "cookie":
            scheme = APIKeyCookie
        elif api_key_spec.type == "query":
            scheme = APIKeyQuery
        else:
            raise Exception
        self.api_key_spec_type = f"api_key_{api_key_spec.type}"
        self.service = service
        self.scheme = scheme(
            name=api_key_spec.api_key.name,
            scheme_name=api_key_spec.api_key.scheme_name,
            description=api_key_spec.api_key.description,
            auto_error=api_key_spec.api_key.auto_error,
        )

    @property
    def dependency(self):
        def api_key_auth(key: Annotated[str, Depends(self.scheme)], request: Request):
            route: APIRoute = request.scope['route']
            headers = {}
            json = {
                "service": self.service,
                "resource": route.path,
                "endpoint": route.name,
                "auth": {
                    "type": self.api_key_spec_type,
                    "key": key,
                }
            }
            self.client.call(headers=headers, json=json)

        return Depends(api_key_auth)
