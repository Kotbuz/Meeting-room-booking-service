from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.rooms import RoomModel
    from app.models.users import UserModel
    from app.models.timeslots import TimeSlotModel


class BookingModel(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    timeslot_id: Mapped[int] = mapped_column(
        ForeignKey("timeslots.id", ondelete="CASCADE")
    )

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))

    date: Mapped[datetime]

    user: Mapped["UserModel"] = relationship(
        back_populates="bookings",
    )

    room: Mapped["RoomModel"] = relationship(
        back_populates="bookings",
    )

    timeslot: Mapped["TimeSlotModel"] = relationship(
        back_populates="bookings",
    )
