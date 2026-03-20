import contextlib
import typing

import fastapi

from ..src.sthali_auth.db import engine, get_session, init_engine


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[None, None]:
    """A context manager that handles the startup and shutdown of Sthali application.

    Args:
        app (fastapi.FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    # init_engine(engine)
    # session = get_session()
    # breakpoint()
    yield


app = fastapi.FastAPI(lifespan=lifespan)


__all__ = [
    "app",
]
