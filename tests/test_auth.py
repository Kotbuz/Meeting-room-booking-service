import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_login_returns_token(client, admin):
    response = await client.post(
        "/api/auth/login",
        data={
            "username": settings.admin_login,
            "password": settings.admin_password,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert body["access_token"]


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    response = await client.get("/api/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, admin_headers):
    response = await client.get(
        "/api/auth/me",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["login"] == settings.admin_login
    assert body["role"] == "admin"
