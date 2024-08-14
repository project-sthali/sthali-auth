"""This module provides security components."""
from collections.abc import Callable
from contextlib import asynccontextmanager
from logging import info
from typing import Any, Literal

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from sthali_crud import AppSpecification as CRUDAppSpecification
from sthali_crud import SthaliCRUD, load_and_parse_spec_file

from .dependencies import APIKey, APIKeyAuth

api_router = APIRouter()


class Auth(BaseModel):
    method: Literal["api_key_header"]


class Authorize(BaseModel):
    service: str
    resource: str
    auth: Auth


@api_router.post("/authorize")
async def authorize(authorize: Authorize) -> None:
    print("authorize")
    print(authorize.model_dump_json())
    return


@dataclass
class AppSpecification:
    """Represents the specification of a SthaliAuth application.

    Attributes:
        service (ServiceSpecification): {...}.
        crud (CRUDAppSpecification): Represents the specification of a SthaliCRUD application.
    """

    # service: Annotated[ServiceSpecification, Field(description="...")]
    crud: CRUDAppSpecification


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    """A context manager that handles the startup and shutdown of SthaliAuth.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    info("Startup SthaliAuth")
    yield
    info("Shutdown SthaliAuth")


class SthaliAuth(SthaliCRUD):
    def __init__(self, app_spec: AppSpecification, lifespan: Callable[..., Any] = default_lifespan) -> None:
        super().__init__(app_spec.crud, lifespan)
        self.app.include_router(api_router)


__all__ = [
    "APIKeyAuth",
    "APIKey",
    "AppSpecification",
    "SthaliAuth",
    "load_and_parse_spec_file",
]
