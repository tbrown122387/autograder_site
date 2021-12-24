import pytest
from app.core.config import settings
from fastapi.testclient import TestClient


def test_post_token_valid_user(client: TestClient, make_test_user):
    login_data = {
        "username": settings.TEST_USER_1_EMAIL,
        "password": settings.TEST_USER_1_PASSWORD,
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert token['access_token']


def test_post_token_invalid_user(client: TestClient):
    login_data = {
        "username": "username",
        "password": "password",
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/token", data=login_data)
    assert response.status_code == 401


def test_post_register_valid_user(client: TestClient):
    register_data = {
        'username': 'username',
        'password': 'password',
        'email': 'new_user@testing.com'
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register", data=register_data)
    data = response.json()
    assert response.status_code == 200
    assert 'email' in data and 'id' in data
    assert data['email'] == 'new_user@testing.com'


def test_post_register_invalid_user(client: TestClient, make_test_user):
    register_data = {
        "username": "username",
        "password": settings.TEST_USER_1_PASSWORD,
        'email': settings.TEST_USER_1_EMAIL
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register", data=register_data)
    assert response.status_code == 400


def test_post_delete_valid_user(client: TestClient, user_token_headers):
    headers = user_token_headers
    response = client.post(
        f"{settings.API_V1_STR}/auth/delete", headers=headers)
    assert response.status_code == 200


@pytest.mark.skip(reason="Not implemented yet")
def test_post_request_password_reset_valid_user():
    pass


@pytest.mark.skip(reason="Not implemented yet")
def test_post_request_password_reset_invalid_user():
    pass


def test_post_reset_password_from_token(client: TestClient, make_test_user):
    get_pw_reset_token = {
        'email': settings.TEST_USER_1_EMAIL,
    }

    response = client.post(f"{settings.API_V1_STR}/auth/request_password_reset", json=get_pw_reset_token)
    pw_reset_token = response.json()['pw_reset_token']

    pw_reset_data = {
        'pw_reset_token': pw_reset_token,
        'email': settings.TEST_USER_1_EMAIL,
        'password': 'password'
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset_password_from_token", data=pw_reset_data)
    user = response.json()

    assert response.status_code == 200
    assert 'email' in user
    assert user['email'] == settings.TEST_USER_1_EMAIL


def test_post_reset_password_logged_in(client: TestClient, user_token_headers):
    headers = user_token_headers
    pw_reset_data = {
        'password': 'password'
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/reset_password_logged_in", headers=headers, data=pw_reset_data)
    assert response.status_code == 200
