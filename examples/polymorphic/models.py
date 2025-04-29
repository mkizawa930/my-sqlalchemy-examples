from enum import StrEnum
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref

from app.db.sqlite import engine

class AddressType(StrEnum):
    Home = "Home"
    Office = "Office"
    Other = "Other"

class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address_type: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": "address_type",
        "polymorphic_identity": "address"
    }


class UserAddress(Address):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="address")
    
    __mapper_args__ = {
        "polymorphic_identity": "user_address"
    }


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped["UserAddress"] = relationship("UserAddress", back_populates="user", cascade="all, delete")

Base.metadata.create_all(engine)


if __name__ == "__main__":
    from sqlalchemy import select
    from app.db.sqlite import Session

    # cascade=all, deleteを設定すると関連付けした親テーブルを子テーブルを削除するタイミングで削除できる
    with Session() as db:
        user = User(name="test", address=UserAddress())
        db.add(user)

        db.commit()
        db.refresh(user)

        print(user, user.address)
        assert user.address.id > 0

        result = db.execute(select(Address)).all()
        assert len(result) == 1

        db.delete(user)
        db.commit()

        assert db.scalar(select(User).where(User.id == user.id)) is None

        result = db.execute(select(Address)).all()
        assert len(result) == 0
        