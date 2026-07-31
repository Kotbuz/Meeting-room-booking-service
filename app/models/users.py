from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

from typing import TYPE_CHECKING

from sqlalchemy import Enum

from app.core.roles import UserRole

if TYPE_CHECKING:
    from app.models.bookings import BookingModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="userrole",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserRole.USER,
        nullable=False,
    )

    bookings: Mapped[list["BookingModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
