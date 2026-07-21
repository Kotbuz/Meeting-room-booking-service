from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
