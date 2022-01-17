import os

from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings


class Settings(BaseSettings):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = os.environ['SECRET_KEY']
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    API_V1_STR: str = "/api/v1"

    PW_RESET_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    TEST_USER_1_EMAIL: str = "test@testing.com"
    TEST_USER_1_PASSWORD: str = "testPassword"

    FRONTEND_URL: str = os.getenv('FRONTEND_URL', 'http://localhost:8080')

    MAIL_PASSWORD: str = os.environ["MAIL_PASSWORD_VAR"]
    MAIL_FROM: str = os.environ["MAIL_FROM_VAR"]
    MAIL_USERNAME: str = os.environ['MAIL_USERNAME_VAR']
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Autograder Bundler"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: str = 'app/templates'


settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER,
)
