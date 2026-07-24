from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies.base_dependencies import SessionDep
from app.models.timeslots import TimeSlotModel
from app.schemas.timeslots import TimeSlotAddSchema

router = APIRouter(tags=["Timeslots"])


@router.post("/timeslots")
async def add_timeslot(data: TimeSlotAddSchema, session: SessionDep):
    new_timeslot = TimeSlotModel(
        start_time=data.start_time, end_time=data.end_time, room_id=data.room_id
    )
    session.add(new_timeslot)
    await session.commit()
    return {"message": "Timeslot added successfully."}


@router.get("/timeslots")
async def get_all_timeslots(session: SessionDep):
    query = select(TimeSlotModel)
    result = await session.execute(query)
    return result.scalars().all()
