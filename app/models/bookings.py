from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BookingModel(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timeslot_id: Mapped[int] = mapped_column(ForeignKey("timeslots.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date: Mapped[datetime]
