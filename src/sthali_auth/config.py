import os

import dotenv

dotenv.load_dotenv()


class Config:
    def __init__(self) -> None:
        sqlalchemy_database_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
        if not isinstance(sqlalchemy_database_uri, str):
            msg = "SQLALCHEMY_DATABASE_URI environment variable is not set"
            raise TypeError(msg)

        self.sqlalchemy_database_uri = sqlalchemy_database_uri


config = Config()