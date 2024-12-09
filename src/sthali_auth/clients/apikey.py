import enum
import typing

import fastapi
import fastapi.security
import pydantic

from . import Base, BaseSpecification, Payload, ServiceClient


@pydantic.dataclasses.dataclass
class APIKeySpecification(BaseSpecification):
    class SchemeEnum(enum.Enum):
        header = fastapi.security.APIKeyHeader
        cookie = fastapi.security.APIKeyCookie
        query = fastapi.security.APIKeyQuery

    scheme: SchemeEnum
    name: str
    scheme_name: str | None = None
    description: str | None = None
    auto_error: bool = True


class APIKeyClient(Base):
    def __init__(
        self, api_key_specification: APIKeySpecification,
    ) -> None:
        self.client = ServiceClient(api_key_specification.service_client_specification)

        self.scheme = api_key_specification.scheme.value(
            name=api_key_specification.name,
            scheme_name=api_key_specification.scheme_name,
            description=api_key_specification.description,
            auto_error=api_key_specification.auto_error,
        )

    @property
    def dependency(self):
        def api_key_auth(key: typing.Annotated[str, fastapi.Depends(self.scheme)], request: fastapi.Request):
            route: fastapi.routing.APIRoute = request.scope["route"]
            headers: dict[str, typing.Any] = {}
            payload = Payload(
                resource=route.path,
                endpoint=route.name,
            )
            print("========================================================================")
            print(payload)
            print("========================================================================")
            # self.client.call(headers, payload)

        return fastapi.Depends(api_key_auth)
