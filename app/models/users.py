from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.bookings import BookingModel


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]

    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="user")
