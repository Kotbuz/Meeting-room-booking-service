from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies.base_dependencies import SessionDep
from app.models.bookings import BookingModel
from app.schemas.bookings import BookingSchema

router = APIRouter()


@router.post("/bookings")
async def add_booking(data: BookingSchema, session: SessionDep):
    new_booking = BookingModel(
        user_id=data.user_id,
        room_id=data.room_id,
        timeslot_id=data.timeslot_id,
        date=data.date,
    )
    session.add(new_booking)
    await session.commit()
    return {"message": "Booking added successfully."}


@router.get("/bookings")
async def get_bookings(session: SessionDep):
    query = select(BookingModel)
    result = await session.execute(query)
    return result.scalars().all()
