from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)

Base: DeclarativeBase = declarative_base()

Session = sessionmaker(bind=engine)
