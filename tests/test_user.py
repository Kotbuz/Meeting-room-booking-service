import pytest


@pytest.mark.asyncio
async def test_create_user(client, admin_headers):
    response = await client.post(
        "/api/users/",
        headers=admin_headers,
        json={
            "login": "test",
            "password": "12345",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["login"] == "test"
    assert body["role"] == "user"


@pytest.mark.asyncio
async def test_get_users_without_token(client):
    response = await client.get("/api/users/")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_get_users(client, user_headers):
    response = await client.get(
        "/api/users/",
        headers=user_headers,
    )

    assert response.status_code == 403
