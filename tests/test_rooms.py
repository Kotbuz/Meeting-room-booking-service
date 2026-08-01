import pytest


@pytest.mark.asyncio
async def test_create_room_as_admin(client, admin_headers):
    response = await client.post(
        "/api/rooms/",
        headers=admin_headers,
        json={
            "name": "Room Alpha",
            "capacity": 10,
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == "Room Alpha"
    assert body["capacity"] == 10


@pytest.mark.asyncio
async def test_create_room_as_user_forbidden(client, user_headers):
    response = await client.post(
        "/api/rooms/",
        headers=user_headers,
        json={
            "name": "Room Beta",
            "capacity": 12,
        },
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_room_by_id_not_found(client):
    response = await client.get("/api/rooms/999999")

    assert response.status_code == 404
