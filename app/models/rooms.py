from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bookings import BookingModel
    from app.models.timeslots import TimeSlotModel


class RoomModel(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    capacity: Mapped[int]

    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="room")
    timeslots: Mapped[list["TimeSlotModel"]] = relationship(back_populates="room")
