"""{...}."""
from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from jwt import decode, encode, exceptions
from pwdlib import PasswordHash
from pydantic import BaseModel, ValidationError
from sthali_db import DBSession

from ..src.sthali_auth.db import User, UserInDB, get_user

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)
password_hash = PasswordHash.recommended()


class Token(BaseModel):
    """{...}."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """{...}."""
    username: str
    scopes: list[str] = []


def authenticate_user(username: str, password: str) -> UserInDB | None:
    """{...}."""
    user = get_user(username)
    if not user:
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDB:
    """{...}."""
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes, username=username)
    except (exceptions.InvalidTokenError, ValidationError) as e:
        raise credentials_exception from e
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
) -> User:
    """{...}."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict[str, Any], expires_delta: datetime.timedelta | None = None) -> str:
    """{...}."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore


class OAuth2:
    """{...}."""

    def __init__(self, config, db_session: DBSession, api) -> None:
        """Initialize the VIEWS handler.

        Args:
        ----
            *args: Positional arguments passed to parent BaseRouter class.
            **kwargs: Keyword arguments passed to parent BaseRouter class.

        """
        self.access_token_expire_minutes = config["access_token_expire_minutes"]
        self.db_session = db_session
        self.api = api

    @property
    def api_router(self) -> APIRouter:
        router = APIRouter(tags=["oauth2", "auth"])
        router.add_api_route(
            "/token",
            self.login_for_access_token,
            response_class=Token,
            methods=["POST"],
        )
        return router

    @api_router.post("/token")
    async def login_for_access_token(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        """{...}."""
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username, "scope": " ".join(form_data.scopes)},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")
