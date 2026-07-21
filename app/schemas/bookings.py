from datetime import datetime

from pydantic import BaseModel


class BookingAddSchema(BaseModel):
    user_id: int
    timeslot_id: int
    room_id: int
    date: datetime


class BookingSchema(BookingAddSchema):
    id: int
