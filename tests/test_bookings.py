from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.asyncio
async def test_create_booking_for_current_user(
    client, admin_headers, user_headers, user
):
    room_response = await client.post(
        "/api/rooms/",
        headers=admin_headers,
        json={
            "name": "Booking Room",
            "capacity": 6,
        },
    )
    room_id = room_response.json()["id"]

    start_time = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=5)
    end_time = start_time + timedelta(hours=1)

    timeslot_response = await client.post(
        "/api/timeslots/",
        headers=admin_headers,
        json={
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    )
    timeslot_id = timeslot_response.json()["id"]

    response = await client.post(
        "/api/bookings/",
        headers=user_headers,
        json={
            "user_id": user.id,
            "room_id": room_id,
            "timeslot_id": timeslot_id,
            "date": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["user_id"] == user.id
    assert body["room_id"] == room_id
    assert body["timeslot_id"] == timeslot_id


@pytest.mark.asyncio
async def test_create_booking_without_token(client):
    response = await client.post(
        "/api/bookings/",
        json={
            "user_id": 1,
            "room_id": 1,
            "timeslot_id": 1,
            "date": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_access_other_user_bookings(client, user_headers, user):
    response = await client.get(
        "/api/bookings/user/999999",
        headers=user_headers,
    )

    assert response.status_code == 403
