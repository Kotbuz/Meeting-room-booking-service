from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


async def get_admin_token(client: AsyncClient) -> str:
    response = await client.post(
        "/api/auth/login",
        data={
            "username": settings.admin_login,
            "password": settings.admin_password,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


async def create_room(client: AsyncClient, token: str, name: str, capacity: int = 10):
    response = await client.post(
        "/api/rooms/",
        json={"name": name, "capacity": capacity},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_timeslot(
    client: AsyncClient,
    token: str,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
):
    response = await client.post(
        "/api/timeslots/",
        json={
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_booking(
    client: AsyncClient,
    token: str,
    room_id: int,
    timeslot_id: int,
    booking_date: datetime,
):
    response = await client.post(
        "/api/bookings/",
        json={
            "user_id": 1,
            "room_id": room_id,
            "timeslot_id": timeslot_id,
            "date": booking_date.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    response = await client.post(
        "/api/auth/login",
        data={
            "username": settings.admin_login,
            "password": settings.admin_password,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


@pytest.mark.asyncio
async def test_create_booking(client: AsyncClient):
    token = await get_admin_token(client)
    room = await create_room(client, token, f"Room-{uuid4().hex[:8]}")

    start_time = datetime(2026, 8, 1, 10, 0, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    timeslot = await create_timeslot(client, token, room["id"], start_time, end_time)

    booking = await create_booking(
        client,
        token,
        room["id"],
        timeslot["id"],
        datetime(2026, 8, 1, tzinfo=timezone.utc),
    )

    assert booking["room_id"] == room["id"]
    assert booking["timeslot_id"] == timeslot["id"]


@pytest.mark.asyncio
async def test_double_booking(client: AsyncClient):
    token = await get_admin_token(client)
    room = await create_room(client, token, f"Room-{uuid4().hex[:8]}")

    start_time = datetime(2026, 8, 2, 10, 0, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    timeslot = await create_timeslot(client, token, room["id"], start_time, end_time)

    await create_booking(
        client,
        token,
        room["id"],
        timeslot["id"],
        datetime(2026, 8, 2, tzinfo=timezone.utc),
    )

    second = await client.post(
        "/api/bookings/",
        json={
            "user_id": 1,
            "room_id": room["id"],
            "timeslot_id": timeslot["id"],
            "date": "2026-08-02T00:00:00+00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert second.status_code == 400
    assert second.json()["detail"] == "Timeslot is already booked"


@pytest.mark.asyncio
async def test_delete_booking(client: AsyncClient):
    token = await get_admin_token(client)
    room = await create_room(client, token, f"Room-{uuid4().hex[:8]}")

    start_time = datetime(2026, 8, 3, 10, 0, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    timeslot = await create_timeslot(client, token, room["id"], start_time, end_time)

    booking = await create_booking(
        client,
        token,
        room["id"],
        timeslot["id"],
        datetime(2026, 8, 3, tzinfo=timezone.utc),
    )

    delete_response = await client.delete(
        f"/api/bookings/{booking['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_permissions(client: AsyncClient):
    admin_token = await get_admin_token(client)
    admin_room = await create_room(client, admin_token, f"Room-{uuid4().hex[:8]}")

    user_login = f"user_{uuid4().hex[:8]}"
    create_user_response = await client.post(
        "/api/users/",
        json={"login": user_login, "password": "secret123"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert create_user_response.status_code == 201, create_user_response.text
    created_user = create_user_response.json()

    login_response = await client.post(
        "/api/auth/login",
        data={"username": user_login, "password": "secret123"},
    )
    assert login_response.status_code == 200, login_response.text
    user_token = login_response.json()["access_token"]

    start_time = datetime(2026, 8, 4, 10, 0, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    timeslot = await create_timeslot(
        client, admin_token, admin_room["id"], start_time, end_time
    )

    booking = await create_booking(
        client,
        user_token,
        admin_room["id"],
        timeslot["id"],
        datetime(2026, 8, 4, tzinfo=timezone.utc),
    )
    assert booking["user_id"] == created_user["id"]

    self_access = await client.get(
        f"/api/bookings/user/{created_user['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert self_access.status_code == 200

    another_user = await client.post(
        "/api/users/",
        json={"login": f"another_{uuid4().hex[:8]}", "password": "secret123"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert another_user.status_code == 201, another_user.text
    other_user_id = another_user.json()["id"]

    forbidden = await client.get(
        f"/api/bookings/user/{other_user_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert forbidden.status_code == 403
