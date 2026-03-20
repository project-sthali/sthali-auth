import datetime
import typing

import fastapi.security
import jwt
import pwdlib
import pydantic

from ..src.sthali_auth.db import User, UserInDB, get_user

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = fastapi.security.OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)
password_hash = pwdlib.PasswordHash.recommended()


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str
    scopes: list[str] = []


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    security_scopes: fastapi.security.SecurityScopes,
    token: typing.Annotated[str, fastapi.Depends(oauth2_scheme)],
) -> UserInDB:
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'

    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes, username=username)
    except (jwt.exceptions.InvalidTokenError, pydantic.ValidationError) as e:
        raise credentials_exception from e
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: typing.Annotated[User, fastapi.Security(get_current_user, scopes=["me"])],
) -> User:
    if current_user.disabled:
        raise fastapi.HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict[str, typing.Any], expires_delta: datetime.timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
