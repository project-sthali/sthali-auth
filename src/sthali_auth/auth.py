import enum
import typing
import importlib

import pydantic
from .clients.apikey import APIKeySpecification


if typing.TYPE_CHECKING:
    from .clients import Base


@pydantic.dataclasses.dataclass
class AuthSpecification:
    class ClientSpecificationEnum(enum.Enum):
        APIKey = APIKeySpecification

    client: str
    specification: ClientSpecificationEnum


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
        client_module = importlib.import_module(f".clients.{auth_spec.client.lower()}", package=__package__)
        client_class: type[Base] = getattr(client_module, f"{auth_spec.client}Client")
        self.dependency = client_class(auth_spec.specification.value).dependency
