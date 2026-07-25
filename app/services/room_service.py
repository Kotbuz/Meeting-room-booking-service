from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


import app.repositories.room_repository as repository
from app.schemas.rooms import RoomCreateSchema, RoomUpdateSchema


async def create_room(session: AsyncSession, data: RoomCreateSchema):
    existing_room = await repository.get_room_by_name(session, data.name)
    if existing_room:
        raise HTTPException(
            status_code=400, detail="Room with this name already exists"
        )
    new_room = await repository.create_room(session, data.name, data.capacity)
    await repository.save(session)
    await repository.refresh(session, new_room)
    return new_room


async def get_room_by_id(session: AsyncSession, id: int):
    return await repository.get_room_by_id(session, id)


async def get_room_by_name(session: AsyncSession, name: str):
    return await repository.get_room_by_name(session, name)


async def get_rooms_by_capacity(session: AsyncSession, capacity: int):
    return await repository.get_room_by_capacity(session, capacity)


async def get_all_rooms(session: AsyncSession):
    return await repository.get_all_rooms(session)


async def update_room(session: AsyncSession, room_id: int, data: RoomCreateSchema):
    room = await repository.get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room does not exists")
    existing_room = await repository.get_room_by_name(session, data.name)
    if existing_room and existing_room.id != room.id:
        raise ValueError("Room with this name already exists")
    updated_room = await repository.update_room(room, data.name, data.capacity)
    await repository.save(session)
    await repository.refresh(session, updated_room)
    return updated_room


async def partial_update_room(
    session: AsyncSession, room_id: int, data: RoomUpdateSchema
):
    room = await repository.get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room does not exists")
    if data.name is not None:
        existing_room = await repository.get_room_by_name(session, data.name)
        if existing_room and existing_room.id != room.id:
            raise ValueError("Room with this name already exists")
    updated_room = await repository.partial_update_room(room, data.name, data.capacity)
    await repository.save(session)
    await repository.refresh(session, updated_room)
    return updated_room


async def delete_room(session: AsyncSession, room_id: int):
    room = await repository.get_room_by_id(session, room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room does not exists")
    await repository.delete_room(session, room)
    await repository.save(session)
    return True
