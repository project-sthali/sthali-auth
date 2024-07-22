"""This module provides the dependencies for sthali-auth usage."""
import typing

import fastapi
import pydantic


async def authorize(req: fastapi.Request) -> typing.NoReturn:
    """Not implemented."""
    # token = req.auth
    raise NotImplementedError
