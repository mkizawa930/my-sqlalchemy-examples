import enum
from datetime import date, datetime
from typing import List
from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, and_, create_engine, select
from sqlalchemy.orm import (
    declarative_base,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    joinedload,
)
from sqlalchemy import func

Base: DeclarativeBase = declarative_base()


class CustomerType(str, enum.Enum):
    individual = enum.auto()
    corporation = enum.auto()


class GenderType(str, enum.Enum):
    male = enum.auto()
    female = enum.auto()
    other = enum.auto()


class ProfileType(str, enum.Enum):
    main = enum.auto()
    sub = enum.auto()


class TimestampMixin(object):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=func.now())


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    prefecture: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped[str] = mapped_column(String, nullable=True)


class Profile(Base):
    __tablename__ = "profiles"

    __mapper_args__ = {
        "polymorphic_on": "entity_type",
        "polymorphic_identity": "profile",
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    address: Mapped[Address] = relationship(Address, cascade="all, delete")


class PersonalProfile(Profile):
    __tablename__ = "personal_profiles"

    __mapper_args__ = {"polymorphic_identity": "personal"}

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False, comment="名")
    last_name: Mapped[str] = mapped_column(String, nullable=False, comment="姓")
    first_name_kana: Mapped[str] = mapped_column(String, nullable=False, comment="名(カナ)")
    last_name_kana: Mapped[str] = mapped_column(String, nullable=False, comment="姓(カナ)")
    gender_type: Mapped[GenderType] = mapped_column(Enum(GenderType), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, comment="誕生日")

    @property
    def full_name(self) -> str:
        return self.last_name + self.first_name

    @property
    def full_name_kana(self) -> str:
        return self.last_name_kana + self.first_name_kana


class CorporateProfile(Profile):
    __tablename__ = "corporate_profiles"

    __mapper_args__ = {"polymorphic_identity": "corporate"}

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    name_kana: Mapped[str] = mapped_column(String, nullable=False)


class CustomerProfile(Base):
    __tablename__ = "customers_profiles"

    __table_args__ = UniqueConstraint("customer_id", "profile_type", "main")

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    profile_type: Mapped[ProfileType] = mapped_column(Enum(ProfileType))
    sequence: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    customer: Mapped["Customer"] = relationship("Customer", back_populates="profiles")
    profile: Mapped[Profile] = relationship(Profile, backref="customer_profile")


class Customer(TimestampMixin, Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_type: Mapped[CustomerType] = mapped_column(Enum(CustomerType), nullable=False)

    main_profile: Mapped[CustomerProfile] = relationship(
        CustomerProfile,
        primaryjoin="and_(Customer.id == CustomerProfile.customer_id, CustomerProfile.profile_type == 'main')",
        uselist=False,
        viewonly=True,  # 読み取り専用
    )

    profiles: Mapped[List[CustomerProfile]] = relationship(CustomerProfile, back_populates="customer", uselist=True)

    @property
    def name(self) -> str:
        return self.main_profile.profile.full_name

    @property
    def name_kana(self) -> str:
        return self.main_profile.profile.full_name_kana


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    customer_profile = CustomerProfile(
        profile_type="main",
        profile=PersonalProfile(
            first_name="太郎",
            last_name="田中",
            first_name_kana="タロウ",
            last_name_kana="タナカ",
            birth_date=date(1980, 1, 1),
            gender_type=GenderType.male,
            address=Address(
                postal_code="123-4567",
                prefecture="東京都",
                city="新宿区",
                street="歌舞伎町1-1-1",
            ),
        ),
    )
    c1 = Customer(customer_type="individual", profiles=[customer_profile])

    with Session() as db:
        db.add(c1)
        db.commit()
        db.refresh(c1)

    with Session() as db:
        stmt = select(Customer).options(joinedload(Customer.main_profile)).where(Customer.id == c1.id)
        result = db.scalar(stmt)
        print("顧客名: {}".format(result.name))
        print("顧客名(カナ): {}".format(result.name_kana))
