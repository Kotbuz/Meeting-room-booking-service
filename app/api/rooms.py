from datetime import date, datetime, time

from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies.auth_dependencies import get_current_admin
from app.dependencies.base_dependencies import SessionDep
import app.services.room_service as service
from app.schemas.rooms import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema

router = APIRouter(tags=["Rooms"])


@router.post(
    "/",
    status_code=201,
    response_model=RoomResponseSchema,
)
async def create_room(
    session: SessionDep,
    data: RoomCreateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.create_room(session, data)


@router.get("/", response_model=list[RoomResponseSchema])
async def get_rooms(
    session: SessionDep,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    capacity: int | None = Query(default=None, ge=1),
    name: str | None = Query(default=None),
):
    return await service.get_all_rooms(
        session,
        limit=limit,
        offset=offset,
        capacity=capacity,
        name=name,
    )


@router.get("/free", response_model=list[RoomResponseSchema])
async def get_free_rooms(
    session: SessionDep,
    date_: date = Query(..., alias="date"),
    start: time = Query(...),
    end: time = Query(...),
    capacity: int | None = Query(default=None, ge=1),
    name: str | None = Query(default=None),
):
    start_datetime = datetime.combine(date_, start)
    end_datetime = datetime.combine(date_, end)

    if start_datetime >= end_datetime:
        raise HTTPException(
            status_code=400,
            detail="Start time must be earlier than end time",
        )

    return await service.get_free_rooms(
        session,
        start_time=start_datetime,
        end_time=end_datetime,
        capacity=capacity,
        name=name,
    )


@router.get("/{id}", response_model=RoomResponseSchema)
async def get_room_by_id(session: SessionDep, id: int):
    room = await service.get_room_by_id(session, id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )
    return room


@router.get("/name/{name}", response_model=RoomResponseSchema)
async def get_room_by_name(session: SessionDep, name: str):
    room = await service.get_room_by_name(session, name)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )
    return room


@router.get("/capacity/{capacity}", response_model=list[RoomResponseSchema])
async def get_rooms_by_capacity(session: SessionDep, capacity: int):
    return await service.get_rooms_by_capacity(session, capacity)


@router.put("/{id}", response_model=RoomResponseSchema)
async def update_room(
    session: SessionDep,
    id: int,
    data: RoomCreateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.update_room(session, id, data)


@router.patch("/{id}", response_model=RoomResponseSchema)
async def partial_update_room(
    session: SessionDep,
    id: int,
    data: RoomUpdateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.partial_update_room(session, id, data)


@router.delete("/{id}", status_code=204)
async def delete_room(
    session: SessionDep,
    id: int,
    current_user=Depends(get_current_admin),
):
    await service.delete_room(session, id)
