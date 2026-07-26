from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookings import BookingModel


async def save(session: AsyncSession):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def refresh(session: AsyncSession, instance):
    await session.refresh(instance)
    return instance


async def create_booking(
    session: AsyncSession,
    user_id: int,
    room_id: int,
    timeslot_id: int,
    date: datetime,
):
    booking = BookingModel(
        user_id=user_id,
        room_id=room_id,
        timeslot_id=timeslot_id,
        date=date,
    )
    session.add(booking)
    return booking


async def get_booking_by_id(session: AsyncSession, booking_id: int):
    return await session.get(BookingModel, booking_id)


async def get_booking_by_timeslot(
    session: AsyncSession,
    timeslot_id: int,
    exclude_id: int | None = None,
):
    query = select(BookingModel).where(BookingModel.timeslot_id == timeslot_id)

    if exclude_id is not None:
        query = query.where(BookingModel.id != exclude_id)

    result = await session.execute(query)
    return result.scalars().first()


async def get_all_bookings(session: AsyncSession):
    result = await session.execute(select(BookingModel))
    return result.scalars().all()


async def update_booking(
    booking: BookingModel,
    user_id: int,
    room_id: int,
    timeslot_id: int,
    date: datetime,
):
    booking.user_id = user_id
    booking.room_id = room_id
    booking.timeslot_id = timeslot_id
    booking.date = date
    return booking


async def partial_update_booking(
    booking: BookingModel,
    user_id: int | None = None,
    room_id: int | None = None,
    timeslot_id: int | None = None,
    date: datetime | None = None,
):
    if user_id is not None:
        booking.user_id = user_id

    if room_id is not None:
        booking.room_id = room_id

    if timeslot_id is not None:
        booking.timeslot_id = timeslot_id

    if date is not None:
        booking.date = date

    return booking


async def delete_booking(
    session: AsyncSession,
    booking: BookingModel,
):
    await session.delete(booking)
