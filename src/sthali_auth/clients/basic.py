# """This module provides the dependencies for sthali-auth usage."""

# import enum
# import typing

# import fastapi
# import fastapi.security
# import pydantic

# from . import ServiceClient


# @pydantic.dataclasses.dataclass
# class HTTPScheme:
#     scheme_name: str | None = None
#     description: str | None = None
#     auto_error: bool = True


# @pydantic.dataclasses.dataclass
# class Basic(HTTPScheme):
#     realm: str | None = None


# @pydantic.dataclasses.dataclass
# class Bearer(HTTPScheme):
#     bearerFormat: str | None = None


# @pydantic.dataclasses.dataclass
# class Digest(HTTPScheme): ...


# @pydantic.dataclasses.dataclass
# class HTTPBasicSpecification:
#     class SchemeEnum(enum.Enum):
#         basic = fastapi.security.HTTPBasic
#         bearer = fastapi.security.HTTPBearer
#         digest = fastapi.security.HTTPDigest

#     scheme: SchemeEnum
#     http: Basic | Bearer | Digest


# class HTTPBasicAuth:
#     client = ServiceClient()

#     def __init__(self, http_basic_spec: HTTPBasicSpecification) -> None:
#         self.basic_spec_scheme = f"http_{http_basic_spec.scheme}"
#         self.scheme = http_basic_spec.scheme.value(
#             scheme_name=http_basic_spec.http.scheme_name,
#             description=http_basic_spec.http.description,
#             auto_error=http_basic_spec.http.auto_error,
#         )

#     @property
#     def dependency(self):
#         def basic(
#             credentials: typing.Annotated[fastapi.security.HTTPBasicCredentials, fastapi.Depends(self.scheme)],
#             request: fastapi.Request,
#         ):
#             route: fastapi.routing.APIRoute = request.scope["route"]
#             headers: dict[str, typing.Any] = {}
#             json: dict[str, typing.Any] = {
#                 "resource": route.path,
#                 "endpoint": route.name,
#                 "auth": {
#                     "type": self.basic_spec_scheme,
#                     "username": credentials.username,
#                     "password": credentials.password,
#                 },
#             }
#             self.client.call(headers=headers, json=json)

#         def authorization(
#             credentials: typing.Annotated[fastapi.security.HTTPAuthorizationCredentials, fastapi.Depends(self.scheme)],
#             request: fastapi.Request,
#         ):
#             route: fastapi.routing.APIRoute = request.scope["route"]
#             headers: dict[str, typing.Any] = {}
#             json: dict[str, typing.Any] = {
#                 # "service": self.service,
#                 "resource": route.path,
#                 "endpoint": route.name,
#                 "auth": {
#                     "type": self.basic_spec_scheme,
#                     "scheme": credentials.scheme,
#                     "credentials": credentials.credentials,
#                 },
#             }
#             self.client.call(headers=headers, json=json)

#         if self.basic_spec_scheme == "basic":
#             return fastapi.Depends(basic)
#         return fastapi.Depends(authorization)
