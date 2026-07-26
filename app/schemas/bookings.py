from datetime import datetime
from pydantic import BaseModel


class BookingCreateSchema(BaseModel):
    user_id: int
    room_id: int
    timeslot_id: int
    date: datetime


class BookingResponseSchema(BaseModel):
    id: int
    user_id: int
    room_id: int
    timeslot_id: int
    date: datetime


class BookingUpdateSchema(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    timeslot_id: int | None = None
    date: datetime | None = None
