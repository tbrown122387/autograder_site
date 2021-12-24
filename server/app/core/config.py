from typing import Set
from pydantic import BaseSettings


class Settings(BaseSettings):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "34dbe0899e7bd0efe165948e2ee5e771cb56d349eca9d9115a4028fa4785c4d6"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"

    TEST_USER_1_EMAIL: str = "test@testing.com"
    TEST_USER_1_PASSWORD: str = "testPassword"


settings = Settings()
