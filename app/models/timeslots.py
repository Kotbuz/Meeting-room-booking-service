from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TimeSlotModel(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(foreign_key="rooms.id")
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
