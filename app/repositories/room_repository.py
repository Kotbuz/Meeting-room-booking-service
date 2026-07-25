from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rooms import RoomModel


async def save(session: AsyncSession):
    try:
        await session.commit()
    except:
        await session.rollback()
        raise


async def refresh(session: AsyncSession, instance):
    await session.refresh(instance)
    return instance


async def get_room_by_id(session: AsyncSession, room_id: int):
    return await session.get(RoomModel, room_id)


async def get_room_by_name(session: AsyncSession, room_name: str):
    query = select(RoomModel).where(RoomModel.name == room_name)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_room_by_capacity(session: AsyncSession, room_capacity: int):
    query = select(RoomModel).where(RoomModel.capacity == room_capacity)
    result = await session.execute(query)
    return result.scalars().all()


async def get_all_rooms(session: AsyncSession):
    query = select(RoomModel)
    result = await session.execute(query)
    return result.scalars().all()


async def create_room(session: AsyncSession, name: str, capacity: str):
    new_room = RoomModel(name=name, capacity=capacity)
    session.add(new_room)
    return new_room


async def update_room(room: RoomModel, name: str, capacity: int):
    room.name = name
    room.capacity = capacity
    return room


async def partial_update_room(room: RoomModel, name: str = None, capacity: int = None):
    if name is not None:
        room.name = name
    if capacity is not None:
        room.capacity = capacity
    return room


async def delete_user(session: AsyncSession, room: RoomModel):
    await session.delete(room)
