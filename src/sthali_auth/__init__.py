# # """This module provides security components."""

# import collections.abc
# import typing

# import fastapi
# import pydantic

# import sthali_backend

# from . import dependencies
# from .clients import Payload, ServiceClientSpecification
# from .clients.api_key import APIKeySpecification
from .config import Config
# from .auth import Auth, AuthSpecification

__all__ = [
    # "Auth",
    # "AuthSpecification",
#     "AppSpecification",
    "Config",
#     "SthaliAuth",
#     "default_lifespan",
#     "dependencies",
]


# default_lifespan = sthali_backend.default_lifespan



# @pydantic.dataclasses.dataclass
# class ResourceSpecification:
#     class AuthorizationSchemeEnum:
#         api_key = "api_key"

#     name: typing.Annotated[str, pydantic.Field(description="The name of the resource")]
#     authorization_scheme: typing.Annotated[AuthorizationSchemeEnum, pydantic.Field(description="Possible authorization methods")]
#     endpoints: typing.Annotated[str, pydantic.Field(description="The name of the resource")]


# @pydantic.dataclasses.dataclass
# class AppSpecification(sthali_backend.AppSpecification):
#     """Represents the specification of a SthaliAuth application."""
#     resources: typing.Annotated[
#         list[ResourceSpecification],
#         pydantic.Field(default_factory=list, description="The list of resource security specifications"),
#     ]

#     def __post_init__(self):  # fix pydantic default values
#         self.title = "SthaliAuth"
#         self.description = "A FastAPI package for implement services."


# class SthaliAuth(sthali_backend.SthaliBackend):
#     """A class to initialize and configure a FastAPI application with {...}.

#     Args:
#         app_specification (AppSpecification): The specification of the application, including title, description, summary,
#             version, dependencies, and resources.
#         lifespan (collections.abc.Callable[..., typing.Any]): The lifespan of the application.
#             Defaults to default_lifespan.
#     """

#     def __init__(
#         self, app_specification: AppSpecification, lifespan: collections.abc.Callable[..., typing.Any] = sthali_backend.default_lifespan
#     ) -> None:
#         """Initializes the SthaliAuth instance.

#         Args:
#             app_specification (AppSpecification): The specification of the application, including title, description, summary,
#                 version, dependencies, and resources.
#             lifespan (collections.abc.Callable[..., typing.Any]): The lifespan of the application.
#                 Defaults to default_lifespan.
#         """
#         super().__init__(app_specification, lifespan)
#         self.app.include_router(authorize_router)


# authorize_router = fastapi.APIRouter()


# @authorize_router.post("/authorize")
# def authorize(payload: Payload) -> None:
#         pass
