from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.bookings import BookingModel
from app.models.rooms import RoomModel


class TimeSlotModel(Base):
    __tablename__ = "timeslots"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="timeslot")
    room: Mapped["RoomModel"] = relationship(back_populates="timeslots")
