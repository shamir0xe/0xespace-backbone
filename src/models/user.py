from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase
from src.models.token import Token


class User(DecoratedBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    email: Mapped[Optional[str]] = mapped_column(
        String, nullable=False, index=True, unique=True
    )
    password: Mapped[bytes]
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    token: Mapped["Token"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
