from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)

TestSession = sessionmaker(bind=engine)

TestSessionLocal = scoped_session(TestSession)
