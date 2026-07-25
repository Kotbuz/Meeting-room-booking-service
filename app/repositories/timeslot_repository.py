from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timeslots import TimeSlotModel


async def save(session: AsyncSession):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def refresh(session: AsyncSession, instance):
    await session.refresh(instance)
    return instance


async def create_timeslot(
    session: AsyncSession, *, room_id: int, start_time: datetime, end_time: datetime
):
    new_timeslot = TimeSlotModel(
        room_id=room_id, start_time=start_time, end_time=end_time
    )
    session.add(new_timeslot)
    return new_timeslot


async def get_timeslot_by_id(session: AsyncSession, timeslot_id: int):
    return await session.get(TimeSlotModel, timeslot_id)


async def get_timeslots_by_room(session: AsyncSession, room_id: int):
    query = (
        select(TimeSlotModel)
        .where(TimeSlotModel.room_id == room_id)
        .order_by(TimeSlotModel.start_time)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_timeslot_by_room_and_time(
    session: AsyncSession,
    room_id: int,
    time: datetime,
):
    query = (
        select(TimeSlotModel)
        .where(TimeSlotModel.room_id == room_id)
        .where(TimeSlotModel.start_time <= time)
        .where(TimeSlotModel.end_time > time)
    )

    result = await session.execute(query)
    return result.scalars().first()


async def get_intersecting_slots(
    session: AsyncSession,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
):
    query = (
        select(TimeSlotModel)
        .where(TimeSlotModel.room_id == room_id)
        .where(TimeSlotModel.start_time < end_time)
        .where(TimeSlotModel.end_time > start_time)
    )

    result = await session.execute(query)
    return result.scalars().all()


async def update_timeslot(
    timeslot: TimeSlotModel, *, room_id: int, start_time: datetime, end_time: datetime
):
    timeslot.room_id = room_id
    timeslot.start_time = start_time
    timeslot.end_time = end_time
    return timeslot


async def partial_update_timeslot(
    timeslot: TimeSlotModel,
    *,
    room_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    if room_id is not None:
        timeslot.room_id = room_id
    if start_time is not None:
        timeslot.start_time = start_time
    if end_time is not None:
        timeslot.end_time = end_time
    return timeslot


async def delete_timeslot(session: AsyncSession, timeslot: TimeSlotModel):
    await session.delete(timeslot)
