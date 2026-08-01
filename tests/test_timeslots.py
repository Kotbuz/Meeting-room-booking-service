from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.asyncio
async def test_create_timeslot_as_admin(client, admin_headers):
    room_response = await client.post(
        "/api/rooms/",
        headers=admin_headers,
        json={
            "name": "Timeslot Room",
            "capacity": 8,
        },
    )
    room_id = room_response.json()["id"]

    start_time = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    response = await client.post(
        "/api/timeslots/",
        headers=admin_headers,
        json={
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["room_id"] == room_id
    assert body["start_time"]
    assert body["end_time"]


@pytest.mark.asyncio
async def test_create_overlapping_timeslot_returns_400(client, admin_headers):
    room_response = await client.post(
        "/api/rooms/",
        headers=admin_headers,
        json={
            "name": "Overlap Room",
            "capacity": 6,
        },
    )
    room_id = room_response.json()["id"]

    start_time = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=2)
    end_time = start_time + timedelta(hours=1)

    first = await client.post(
        "/api/timeslots/",
        headers=admin_headers,
        json={
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    )
    assert first.status_code == 201

    second = await client.post(
        "/api/timeslots/",
        headers=admin_headers,
        json={
            "room_id": room_id,
            "start_time": (start_time + timedelta(minutes=30)).isoformat(),
            "end_time": (end_time + timedelta(minutes=30)).isoformat(),
        },
    )

    assert second.status_code == 400


@pytest.mark.asyncio
async def test_create_timeslot_as_user_forbidden(client, user_headers):
    response = await client.post(
        "/api/timeslots/",
        headers=user_headers,
        json={
            "room_id": 1,
            "start_time": (
                datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=3)
            ).isoformat(),
            "end_time": (
                datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=4)
            ).isoformat(),
        },
    )

    assert response.status_code == 403
