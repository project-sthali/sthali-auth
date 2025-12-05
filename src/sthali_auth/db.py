import logging
import typing

import sqlalchemy
import sqlmodel
import tenacity

from .config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1

engine = sqlmodel.create_engine(config.sqlalchemy_database_uri)


def get_session() -> typing.Generator[sqlmodel.Session, None, None]:
    with sqlmodel.Session(engine) as session:
        yield session


@tenacity.retry(
    stop=tenacity.stop_after_attempt(MAX_TRIES),
    wait=tenacity.wait_fixed(WAIT_SECONDS),
    before=tenacity.before_log(logger, logging.INFO),
    after=tenacity.after_log(logger, logging.WARN),
)
def init_engine(db_engine: sqlalchemy.Engine) -> None:
    try:
        get_session()
    except Exception as e:
        logger.error(e)
        raise e


def init_db(session: sqlmodel.Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    return
    # user = session.exec(
    #     select(User).where(User.email == settings.FIRST_SUPERUSER)
    # ).first()
    # if not user:
    #     user_in = UserCreate(
    #         email=settings.FIRST_SUPERUSER,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #     )
    #     user = crud.create_user(session=session, user_create=user_in)
