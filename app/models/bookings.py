from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.rooms import RoomModel
from app.models.timeslots import TimeSlotModel
from app.models.users import UserModel


class BookingModel(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timeslot_id: Mapped[int] = mapped_column(ForeignKey("timeslots.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date: Mapped[datetime]

    user: Mapped["UserModel"] = relationship(back_populates="bookings")
    timeslot: Mapped["TimeSlotModel"] = relationship(back_populates="bookings")
    room: Mapped["RoomModel"] = relationship(back_populates="bookings")
