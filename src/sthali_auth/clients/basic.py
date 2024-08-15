"""This module provides the dependencies for sthali-auth usage."""
from typing import Annotated, Literal

from fastapi import Depends, Request
from fastapi.routing import APIRoute
from fastapi.security import HTTPBasic, HTTPBearer, HTTPDigest, HTTPBasicCredentials, HTTPAuthorizationCredentials
from pydantic.dataclasses import dataclass

from . import ServiceClient


@dataclass
class Basic:
    scheme_name: str | None = None
    # realm: str | None = None
    description: str | None = None
    auto_error: bool = True


@dataclass
class Bearer:
    # bearerFormat: str | None = None
    scheme_name: str | None = None
    description: str | None = None
    auto_error: bool = True


@dataclass
class Digest:
    scheme_name: str | None = None
    description: str | None = None
    auto_error: bool = True


@dataclass
class HTTPSpecification:
    type: Literal["basic", "bearer", "digest"]
    http: Basic | Bearer | Digest


class HTTPBasicAuth:
    client = ServiceClient()

    def __init__(self, http_spec: HTTPSpecification, service: str) -> None:
        if http_spec.type == "basic":
            scheme = HTTPBasic
        elif http_spec.type == "bearer":
            scheme = HTTPBearer
        elif http_spec.type == "digest":
            scheme = HTTPDigest
        else:
            raise Exception
        self.basic_spec_type = f"http_{http_spec.type}"
        self.service = service
        self.scheme = scheme(
            scheme_name=http_spec.http.scheme_name,
            description=http_spec.http.description,
            auto_error=http_spec.http.auto_error,
        )

    @property
    def dependency(self):
        def basic(credentials: Annotated[HTTPBasicCredentials, Depends(self.scheme)], request: Request):
            route: APIRoute = request.scope["route"]
            headers = {}
            json = {
                "service": self.service,
                "resource": route.path,
                "endpoint": route.name,
                "auth": {
                    "type": self.basic_spec_type,
                    "username": credentials.username,
                    "password": credentials.password,
                },
            }
            self.client.call(headers=headers, json=json)

        def authorization(credentials: Annotated[HTTPAuthorizationCredentials, Depends(self.scheme)], request: Request):
            route: APIRoute = request.scope["route"]
            headers = {}
            json = {
                "service": self.service,
                "resource": route.path,
                "endpoint": route.name,
                "auth": {
                    "type": self.basic_spec_type,
                    "scheme": credentials.scheme,
                    "credentials": credentials.credentials,
                },
            }
            self.client.call(headers=headers, json=json)

        if self.basic_spec_type == "basic":
            return Depends(basic)
        return Depends(authorization)
