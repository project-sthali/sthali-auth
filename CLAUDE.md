# sthali-auth

FastAPI authentication library for the Sthali ecosystem. Provides API Key (cookie/header/query) and HTTP (basic/bearer) authentication dependencies, plus SQLAlchemy User/Role models with many-to-many relationships.

## Project Structure

```
src/sthali_auth/
├── __init__.py             # SthaliAuth factory, Types enum, exports definitions
├── config.py               # ConfigSchema (auth.api_key / auth.oauth2 sub-schemas)
├── models.py               # UserModel, RoleModel, user_roles M2M table
├── schemas.py              # User/Role Create/Read/Update Pydantic schemas
├── dependencies/
│   ├── __init__.py         # Base dependency class
│   ├── api_key.py          # APIKey: cookie/header/query variants
│   ├── http.py             # HTTP: basic/bearer variants
│   └── oauth2.py           # OAuth2: incomplete, broken imports — DO NOT USE
└── routers/
    ├── __init__.py         # Empty
    └── oauth2.py           # OAuth2 token endpoint — incomplete, broken imports
BKP/                        # Legacy backup files — ignore
alembic/                    # DB migration scripts
```

## Key Concepts

- **`SthaliAuth`** — Factory class. `SthaliAuth.from_type(_type, definition)` instantiates the correct auth dependency (`APIKey` or `HTTP`) and sets `self.client` to the dependency instance.
- **`APIKey`** — Wraps FastAPI's `APIKeyCookie`/`APIKeyHeader`/`APIKeyQuery`. `from_type(type, name, ...)` creates the instance. `.dependency` returns `Annotated[str, Depends(fastapi_security_obj)]`.
- **`HTTP`** — Wraps FastAPI's `HTTPBasic`/`HTTPBearer`. `.dependency` returns the annotated type.
- **`definitions`** — Module-level `definitions_type` list: `[(UserModel, (UserCreateSchema, UserReadSchema, UserUpdateSchema)), (RoleModel, ...)]`. Used by `sthali-backend` to register auth CRUD routes.
- **`UserModel`** / **`RoleModel`** — SQLAlchemy ORM models with UUID PKs and a M2M `user_roles` association table.

## Config Schema (YAML)

```yaml
auth:
  api_key:
    type: header       # cookie | header | query
    name: x-api_key
    scheme_name: null  # optional
    description: null  # optional
    auto_error: null   # optional, defaults to true
  oauth2:
    access_token_expire_minutes: 30
```

## Dependency Chain

`sthali-db` → `sthali-auth`

## Python Version

Requires Python >= 3.10.

## Known Issues / TODOs

- `routers/oauth2.py` imports from `..src.sthali_auth.db` which does not exist — this file is broken and non-functional. It was ported from old FastAPI docs examples and needs a complete rewrite.
- `dependencies/oauth2.py` has the same broken import problem.
- `SthaliAuth.__init__` uses `match _type:` but `_type` is a string — the `Types` enum exists but is never used for matching. The match should use `_type.value` or compare against enum members.
- `{...}` placeholder docstrings throughout.
- No tests exist.

## Testing

```bash
cd /home/jhunu/sth/sthali-auth
/home/jhunu/sth/.venv/bin/python -m pytest tests/ -v
```

## Linting

```bash
/home/jhunu/sth/.venv/bin/ruff check src/
```

## Key Rules for AI

- **Do not touch `routers/oauth2.py` or `dependencies/oauth2.py`** without a full rewrite plan — they have broken imports and dead code.
- `definitions` is a module-level variable (not a class member) — it's imported directly by `sthali-backend`.
- `Base.dependency` is a property returning `Annotated[type, Depends(callable)]` — the pattern is intentional for FastAPI's DI system.
- `UserModel.__tablename__ = "users"` and `RoleModel.__tablename__ = "roles"` — these are used as route prefixes in the CRUD layer.
