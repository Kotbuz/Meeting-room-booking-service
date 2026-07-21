from datetime import datetime

from pydantic import BaseModel


class TimeSlotAddSchema(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime


class TimeSlotSchema(TimeSlotAddSchema):
    id: int
