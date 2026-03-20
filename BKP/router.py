import datetime
import typing

import fastapi
import fastapi.security

from .db import User
from .oauth2 import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
)

api_router = fastapi.APIRouter()


@api_router.post("/token")
async def login_for_access_token(
    form_data: typing.Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise fastapi.HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scope": " ".join(form_data.scopes)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@api_router.get("/users/me/")
async def read_users_me(
    current_user: typing.Annotated[User, fastapi.Depends(get_current_active_user)],
) -> User:
    return current_user


@api_router.get("/users/me/items/")
async def read_own_items(
    current_user: typing.Annotated[User, fastapi.Security(get_current_active_user, scopes=["items"])],
) -> list[dict[str, str]]:
    return [{"item_id": "Foo", "owner": current_user.username}]


@api_router.get("/status/")
async def read_system_status(
    current_user: typing.Annotated[User, fastapi.Depends(get_current_user)],
) -> dict[str, str]:
    return {"status": "ok"}
