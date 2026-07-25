from datetime import datetime

from fastapi import APIRouter, HTTPException
from app.dependencies.base_dependencies import SessionDep
import app.services.timeslot_service as service
from app.schemas.timeslots import (
    TimeSlotCreateSchema,
    TimeSlotResponseSchema,
    TimeSlotUpdateSchema,
)

router = APIRouter(tags=["Timeslots"])


@router.post("/", status_code=201, response_model=TimeSlotResponseSchema)
async def add_timeslot(session: SessionDep, data: TimeSlotCreateSchema):
    return await service.create_timeslot(session, data)


@router.get("/", response_model=list[TimeSlotResponseSchema])
async def get_timeslots(session: SessionDep):
    return await service.get_all_timeslots(session)


@router.get("/{id}", response_model=TimeSlotResponseSchema)
async def get_timeslot_by_id(session: SessionDep, id: int):
    timeslot = await service.get_timeslot_by_id(session, id)
    if not timeslot:
        raise HTTPException(
            status_code=404,
            detail="Timeslot not found",
        )
    return timeslot


@router.get("/roomtime/{room_id}/{time}", response_model=TimeSlotResponseSchema)
async def get_timeslot_by_room_and_time(
    session: SessionDep, room_id: int, time: datetime
):
    timeslot = await service.get_timeslot_by_room_and_time(session, room_id, time)
    if not timeslot:
        raise HTTPException(
            status_code=404,
            detail="Timeslot not found",
        )
    return timeslot


@router.get(
    "/roomstartend/{room_id}/{start_time}/{end_time}",
    response_model=list[TimeSlotResponseSchema],
)
async def get_intersecting_timeslots(
    session: SessionDep, room_id: int, start_time: datetime, end_time: datetime
):
    return await service.get_intersecting_timeslots(
        session, room_id, start_time, end_time
    )


@router.put("/{id}", response_model=TimeSlotResponseSchema)
async def update_timeslot(
    session: SessionDep,
    id: int,
    data: TimeSlotCreateSchema,
):
    return await service.update_timeslot(session, id, data)


@router.patch("/{id}", response_model=TimeSlotResponseSchema)
async def partial_update_timeslot(
    session: SessionDep, id: int, data: TimeSlotUpdateSchema
):
    return await service.partial_update_timeslot(session, id, data)


@router.delete("/{id}", status_code=204)
async def delete_timeslot(session: SessionDep, id: int):
    await service.delete_timeslot(session, id)
