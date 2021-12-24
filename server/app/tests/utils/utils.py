from fastapi.testclient import TestClient

from app.core.config import settings


def get_token_headers(client: TestClient):
    login_data = {
        "username": settings.TEST_USER_1_EMAIL,
        "password": settings.TEST_USER_1_PASSWORD,
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
