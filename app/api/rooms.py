from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies.base_dependencies import SessionDep
from app.models.rooms import RoomModel
from app.schemas.rooms import RoomAddSchema

router = APIRouter(tags=["Rooms"])


@router.post("/rooms")
async def add_room(data: RoomAddSchema, session: SessionDep):
    new_room = RoomModel(name=data.name, capacity=data.capacity)
    session.add(new_room)
    await session.commit()
    return {"message": "Room added successfully."}


@router.get("/rooms")
async def get_all_rooms(session: SessionDep):
    query = select(RoomModel)
    result = await session.execute(query)
    return result.scalars().all()
