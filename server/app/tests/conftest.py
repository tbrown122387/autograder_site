from typing import Generator

import pytest
from app.db import engine
from app.main import app
from app.core.config import settings
from app.core import security
from app.crud import crud_user
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.tests.utils.utils import get_token_headers


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def session() -> Generator:
    with Session(engine) as session:
        yield session


@pytest.fixture
def make_test_user(session):
    # creates a test user that can be used for testing
    user = crud_user.get_user_from_email(session, settings.TEST_USER_1_EMAIL)
    if user:
        crud_user.reset_password(session, email=settings.TEST_USER_1_EMAIL, password=settings.TEST_USER_1_PASSWORD)
    else:  # create user
        hashed_password = security.get_password_hash(
            settings.TEST_USER_1_PASSWORD)
        user = User(email=settings.TEST_USER_1_EMAIL,
                    hash_password=hashed_password, username="test", name="test")
        crud_user.create_user(session, user)


@pytest.fixture
def user_token_headers(client: TestClient, make_test_user):
    # ensures a test user is created before getting the headers
    return get_token_headers(client)
