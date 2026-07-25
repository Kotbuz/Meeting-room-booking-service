from fastapi import APIRouter, HTTPException
from app.dependencies.base_dependencies import SessionDep
import app.services.room_service as service
from app.schemas.rooms import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema

router = APIRouter(tags=["Rooms"])


@router.post("/", status_code=201, response_model=RoomResponseSchema)
async def add_room(session: SessionDep, data: RoomCreateSchema):
    return await service.create_room(session, data)


@router.get("/", response_model=list[RoomResponseSchema])
async def get_rooms(session: SessionDep):
    return await service.get_all_rooms(session)


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
):
    return await service.update_room(session, id, data)


@router.patch("/{id}", response_model=RoomResponseSchema)
async def partial_update_room(session: SessionDep, id: int, data: RoomUpdateSchema):
    return await service.partial_update_room(session, id, data)


@router.delete("/{id}", status_code=204)
async def delete_room(session: SessionDep, id: int):
    await service.delete_room(session, id)
