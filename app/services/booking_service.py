from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.repositories.booking_repository as repository
from app.repositories import (
    room_repository,
    timeslot_repository,
    user_repository,
)

from app.schemas.bookings import (
    BookingCreateSchema,
    BookingUpdateSchema,
)

from datetime import datetime


def normalize_datetime(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_booking(session: AsyncSession, data: BookingCreateSchema):
    user = await user_repository.get_user_by_id(session, data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    room = await room_repository.get_room_by_id(session, data.room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    timeslot = await timeslot_repository.get_timeslot_by_id(
        session,
        data.timeslot_id,
    )
    if not timeslot:
        raise HTTPException(
            status_code=404,
            detail="Timeslot not found",
        )

    if timeslot.room_id != data.room_id:
        raise HTTPException(
            status_code=400,
            detail="Timeslot does not belong to this room",
        )

    existing_booking = await repository.get_booking_by_timeslot(
        session,
        data.timeslot_id,
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Timeslot is already booked",
        )

    new_booking = await repository.create_booking(
        session,
        user_id=data.user_id,
        room_id=data.room_id,
        timeslot_id=data.timeslot_id,
        date=normalize_datetime(data.date),
    )

    await repository.save(session)
    await repository.refresh(session, new_booking)
    return new_booking


async def get_booking_by_id(session: AsyncSession, booking_id: int):
    return await repository.get_booking_by_id(session, booking_id)


async def get_bookings_by_user(session: AsyncSession, user_id: int):
    user = await user_repository.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repository.get_bookings_by_user(session, user_id)


async def get_all_bookings(session: AsyncSession):
    return await repository.get_all_bookings(session)


async def update_booking(
    session: AsyncSession,
    booking_id: int,
    data: BookingCreateSchema,
):
    booking = await repository.get_booking_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    user = await user_repository.get_user_by_id(session, data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    room = await room_repository.get_room_by_id(session, data.room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    timeslot = await timeslot_repository.get_timeslot_by_id(
        session,
        data.timeslot_id,
    )
    if not timeslot:
        raise HTTPException(
            status_code=404,
            detail="Timeslot not found",
        )

    if timeslot.room_id != data.room_id:
        raise HTTPException(
            status_code=400,
            detail="Timeslot does not belong to this room",
        )

    existing_booking = await repository.get_booking_by_timeslot(
        session,
        data.timeslot_id,
        exclude_id=booking.id,
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Timeslot is already booked",
        )

    updated_booking = await repository.update_booking(
        booking,
        user_id=data.user_id,
        room_id=data.room_id,
        timeslot_id=data.timeslot_id,
        date=normalize_datetime(data.date),
    )

    await repository.save(session)
    await repository.refresh(session, updated_booking)
    return updated_booking


async def partial_update_booking(
    session: AsyncSession,
    booking_id: int,
    data: BookingUpdateSchema,
):
    booking = await repository.get_booking_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    new_user_id = data.user_id or booking.user_id
    new_room_id = data.room_id or booking.room_id
    new_timeslot_id = data.timeslot_id or booking.timeslot_id

    user = await user_repository.get_user_by_id(session, new_user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    room = await room_repository.get_room_by_id(session, new_room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    timeslot = await timeslot_repository.get_timeslot_by_id(
        session,
        new_timeslot_id,
    )
    if not timeslot:
        raise HTTPException(
            status_code=404,
            detail="Timeslot not found",
        )

    if timeslot.room_id != new_room_id:
        raise HTTPException(
            status_code=400,
            detail="Timeslot does not belong to this room",
        )

    existing_booking = await repository.get_booking_by_timeslot(
        session,
        new_timeslot_id,
        exclude_id=booking.id,
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Timeslot is already booked",
        )

    updated_booking = await repository.partial_update_booking(
        booking,
        user_id=data.user_id,
        room_id=data.room_id,
        timeslot_id=data.timeslot_id,
        date=normalize_datetime(data.date),
    )

    await repository.save(session)
    await repository.refresh(session, updated_booking)
    return updated_booking


async def delete_booking(
    session: AsyncSession,
    booking_id: int,
):
    booking = await repository.get_booking_by_id(session, booking_id)

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    await repository.delete_booking(session, booking)
    await repository.save(session)
    return True
