from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)

    primary_address: Mapped["UserAddress"] = relationship(
        "UserAddress",
        back_populates="user",
        primaryjoin="and_(User.id == UserAddress.user_id, UserAddress.sequence == 1)",
        overlaps="user_addresses",
    )

    user_addresses: Mapped[List["UserAddress"]] = relationship(
        "UserAddress",
        back_populates="user",
        order_by="UserAddress.sequence",
    )

    def __str__(self):
        return f"User(email={self.email}), username={self.username}"


class UserAddress(Base):
    __tablename__ = "addresses"

    __table_args__ = (UniqueConstraint("user_id", "sequence"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sequence: Mapped[int] = mapped_column(nullable=False, default=1)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=False)
    prefecture: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="user_addresses")
