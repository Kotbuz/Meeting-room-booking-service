from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories import room_repository
import app.repositories.timeslot_repository as repository
from app.schemas.timeslots import TimeSlotCreateSchema, TimeSlotUpdateSchema


def validate_time_interval(start_time: datetime, end_time: datetime):
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be earlier than end time",
        )


def normalize_datetime(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def validate_start_time(start_time: datetime):
    if normalize_datetime(start_time) <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Start time cannot be in the past",
        )


async def create_timeslot(session: AsyncSession, data: TimeSlotCreateSchema):

    room = await room_repository.get_room_by_id(session, data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    validate_start_time(data.start_time)
    validate_time_interval(data.start_time, data.end_time)
    existing_timeslot = await repository.get_intersecting_timeslots(
        session,
        data.room_id,
        normalize_datetime(data.start_time),
        normalize_datetime(data.end_time),
    )
    if existing_timeslot:
        raise HTTPException(
            status_code=400,
            detail="TimeSlot overlaps with another timeslot",
        )
    new_timeslot = await repository.create_timeslot(
        session,
        data.room_id,
        normalize_datetime(data.start_time),
        normalize_datetime(data.end_time),
    )
    await repository.save(session)
    await repository.refresh(session, new_timeslot)
    return new_timeslot


async def get_timeslot_by_id(session: AsyncSession, id: int):
    return await repository.get_timeslot_by_id(session, id)


async def get_timeslot_by_room_and_time(
    session: AsyncSession,
    room_id: int,
    time: datetime,
):
    room = await room_repository.get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return await repository.get_timeslot_by_room_and_time(
        session, room_id, normalize_datetime(time)
    )


async def get_intersecting_timeslots(
    session: AsyncSession,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
):

    room = await room_repository.get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    validate_time_interval(start_time, end_time)
    return await repository.get_intersecting_timeslots(
        session, room_id, normalize_datetime(start_time), normalize_datetime(end_time)
    )


async def get_all_timeslots(session: AsyncSession):
    return await repository.get_all_timeslots(session)


async def update_timeslot(
    session: AsyncSession, timeslot_id: int, data: TimeSlotCreateSchema
):
    room = await room_repository.get_room_by_id(session, data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    validate_start_time(data.start_time)
    validate_time_interval(data.start_time, data.end_time)
    timeslot = await repository.get_timeslot_by_id(session, timeslot_id)
    if not timeslot:
        raise HTTPException(status_code=404, detail="Timeslot does not exist")

    intersections = await repository.get_intersecting_timeslots(
        session,
        data.room_id,
        normalize_datetime(data.start_time),
        normalize_datetime(data.end_time),
        exclude_id=timeslot.id,
    )

    if intersections:
        raise HTTPException(
            status_code=400,
            detail="TimeSlot overlaps with another timeslot",
        )
    updated_timeslot = await repository.update_timeslot(
        timeslot,
        room_id=data.room_id,
        start_time=normalize_datetime(data.start_time),
        end_time=normalize_datetime(data.end_time),
    )
    await repository.save(session)
    await repository.refresh(session, updated_timeslot)
    return updated_timeslot


async def partial_update_timeslot(
    session: AsyncSession, timeslot_id: int, data: TimeSlotUpdateSchema
):

    timeslot = await repository.get_timeslot_by_id(session, timeslot_id)
    if not timeslot:
        raise HTTPException(status_code=404, detail="Timeslot does not exist")

    new_room_id = data.room_id if data.room_id is not None else timeslot.room_id
    new_start = data.start_time if data.start_time is not None else timeslot.start_time
    new_end = data.end_time if data.end_time is not None else timeslot.end_time

    validate_start_time(new_start)

    room = await room_repository.get_room_by_id(session, new_room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    validate_time_interval(new_start, new_end)

    intersections = await repository.get_intersecting_timeslots(
        session,
        new_room_id,
        normalize_datetime(new_start),
        normalize_datetime(new_end),
        exclude_id=timeslot.id,
    )

    if intersections:
        raise HTTPException(
            status_code=400,
            detail="TimeSlot overlaps with another timeslot",
        )
    updated_timeslot = await repository.partial_update_timeslot(
        timeslot,
        room_id=data.room_id,
        start_time=normalize_datetime(data.start_time),
        end_time=normalize_datetime(data.end_time),
    )
    await repository.save(session)
    await repository.refresh(session, updated_timeslot)
    return updated_timeslot


async def delete_timeslot(session: AsyncSession, timeslot_id: int):
    timeslot = await repository.get_timeslot_by_id(session, timeslot_id)

    if not timeslot:
        raise HTTPException(status_code=404, detail="Timeslot does not exist")

    await repository.delete_timeslot(session, timeslot)
    await repository.save(session)
    return True
