import pathlib
import typing

import pydantic
import sthali_core

from .clients import BaseSpecification

if typing.TYPE_CHECKING:
    from .clients import Base

enum_clients_config = sthali_core.enum_clients.Config(__package__, pathlib.Path("clients"))
ClientEnum = enum_clients_config.ClientEnum


@pydantic.dataclasses.dataclass
class AuthSpecification:
    client: ClientEnum
    specification: BaseSpecification

    @pydantic.model_validator(mode="before")
    @classmethod
    def validate_before(cls, data: typing.Any) -> typing.Any:
        client = getattr(ClientEnum, data['client']).name
        breakpoint()
        return data

    @pydantic.model_validator(mode="after")
    @classmethod
    def validate_after(cls, data: typing.Any) -> typing.Any:
        breakpoint()
        return data


class Auth:
    """Represents a authorizer client adapter.

    Args:
        auth_spec (AuthSpecification): The specification for the ....
    """

    def __init__(self, auth_spec: AuthSpecification) -> None:
        """Initialize the Auth instance.

        Args:
            auth_spec (AuthSpecification): The specification for the ....
        """
        client_module = enum_clients_config.clients_map[auth_spec.client.name]
        client_class: type[Base] = getattr(client_module, f"{auth_spec.client.name.title()}Client")
        self.dependency = client_class(auth_spec.specification).dependency
