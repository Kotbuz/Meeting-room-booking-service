from datetime import datetime

from pydantic import BaseModel


class TimeSlotCreateSchema(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime


class TimeSlotSchema(TimeSlotCreateSchema):
    id: int


class TimeSlotResponseSchema(BaseModel):
    id: int
    room_id: int
    start_time: datetime
    end_time: datetime


class TimeSlotUpdateSchema(BaseModel):
    room_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
