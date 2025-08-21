import typing

import httpx
import pydantic


@pydantic.dataclasses.dataclass
class ServiceClientSpecification:
    url: str


@pydantic.dataclasses.dataclass
class BaseSpecification:
    service_client_specification: ServiceClientSpecification


class Base:
    def __init__(self, specification: type[BaseSpecification]) -> None:
        pass

    @property
    def dependency(self) -> typing.Any:
        raise NotImplementedError


@pydantic.dataclasses.dataclass
class Payload:
    resource: str
    endpoint: str


class ServiceClient:
    def __init__(self, service_client_specification: ServiceClientSpecification) -> None:
        self.url = service_client_specification.url

    def call(self, headers: dict[str, typing.Any], payload: Payload) -> None:
        json = payload.__dict__
        httpx.post(self.url, headers=headers, json=json)
