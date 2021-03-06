import os
from typing import Optional

from sqlmodel import create_engine


def get_database_uri() -> str:
    DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        # local
        POSTGRES_USER = os.environ.get('POSTGRES_USER')
        POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        POSTGRES_DB = os.environ.get('POSTGRES_DB')
        POSTGRES_ADDRESS = os.environ.get('POSTGRES_ADDRESS')

        # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
        DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:5432/{POSTGRES_DB}"
    elif DATABASE_URL.startswith("postgres://"):
        # prod
        # Change in SQLAlchemy 1.4
        # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql+psycopg2://")
    return DATABASE_URL


DATABASE_URL = get_database_uri()


engine = create_engine(DATABASE_URL, echo=False)
