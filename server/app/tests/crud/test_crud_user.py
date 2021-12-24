from os import name

from _pytest.compat import ascii_escaped
from app import crud
from app.core import security
from app.core.config import settings
from sqlmodel import Session
from app.models import User
from app.crud import crud_user


def test_reset_password_valid(session: Session, make_test_user):
    user = crud_user.reset_password(session, email=settings.TEST_USER_1_EMAIL, password="password")
    assert user
    assert user.email == settings.TEST_USER_1_EMAIL
    assert hasattr(user, "hash_password")
    assert security.verify_password(plain_password="password", hashed_password=user.hash_password)


def test_reset_password_invalid(session: Session, make_test_user):
    user = crud_user.reset_password(session, email="dne@dne.com", password="password")
    assert not user


def test_authenticate_user_valid(session: Session, make_test_user):
    user = crud_user.authenticate_user(session, username=settings.TEST_USER_1_EMAIL,
                                       password=settings.TEST_USER_1_PASSWORD)
    assert user
    assert user.email == settings.TEST_USER_1_EMAIL


def test_authenticate_user_invalid_email(session: Session):
    user = crud_user.authenticate_user(session, username="dne@dne.com",
                                       password="password")
    assert not user


def test_authenticate_user_invalid_password(session: Session, make_test_user):
    user = crud_user.authenticate_user(session, username=settings.TEST_USER_1_EMAIL,
                                       password="password")
    assert not user


def test_get_user_from_email_valid(session: Session, make_test_user):
    user = crud_user.get_user_from_email(session, settings.TEST_USER_1_EMAIL)
    assert user
    assert user.email == settings.TEST_USER_1_EMAIL


def test_get_user_from_email_invalid(session: Session):
    user = crud_user.get_user_from_email(session, email="dne@dne.com")
    assert not user


def test_delete_user_from_id_valid(session: Session, make_test_user):
    user_to_delete = crud_user.get_user_from_email(session, email=settings.TEST_USER_1_EMAIL)
    assert user_to_delete
    user = crud_user.delete_user_from_id(session, id=user_to_delete.id)
    assert user
    assert user.email == settings.TEST_USER_1_EMAIL


def test_create_user(session: Session):
    password = "password"
    hashed_password = security.get_password_hash(password)
    user_to_create = User(email="email@email.com", hash_password=hashed_password, username="username", name="name")
    user = crud_user.create_user(session, user_to_create)
    assert user
    assert user.email == "email@email.com"
