from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BookingModel(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    timeslot_id: Mapped[int] = mapped_column(foreign_key="timeslots.id")
    room_id: Mapped[int] = mapped_column(foreign_key="rooms.id")
    date: Mapped[datetime]
