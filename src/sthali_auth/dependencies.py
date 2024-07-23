from typing import Annotated, Any, Literal

from fastapi import Depends, Request
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery
from httpx import post
from pydantic.dataclasses import dataclass


class ServiceClient:
    def __init__(self) -> None:
        self.url = "localhost:8000/authorize"

    def call(self, headers: dict[str, Any], json: dict[str, Any]) -> None:
        post(self.url, headers=headers, json=json)


@dataclass
class APIKey:
    name: str
    scheme_name: str | None = None
    description: str | None = None
    auto_error: bool = True


@dataclass
class APIKeyScheme:
    header = APIKeyHeader
    cookie = APIKeyCookie
    query = APIKeyQuery


class APIKeyAuth:
    client = ServiceClient()

    def __init__(self, api_key: APIKey, type: Literal["header", "cookie", "query"], service: str) -> None:
        scheme = getattr(APIKeyScheme, type)
        self.type = type
        self.service = service
        self.scheme = scheme(
            name=api_key.name,
            scheme_name=api_key.scheme_name,
            description=api_key.description,
            auto_error=api_key.auto_error,
        )

    @property
    def dependency(self):
        def api_key_auth(key: Annotated[str, Depends(self.scheme)], request: Request):
            print("api_key_auth")
            # headers = {"X-API-Key": key}
            # json = {"service": self.service, "resource": request.url.path, "auth": {"": f"api_key_{self.type}"}}
            # self.client.call(headers=headers, json=json)

        return Depends(api_key_auth)
