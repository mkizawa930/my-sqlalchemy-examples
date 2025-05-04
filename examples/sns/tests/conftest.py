from typing import Any, Generator
import pytest
from sqlalchemy.orm import Session

from sns.models import Base

from .database import TestSessionLocal, engine


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db() -> Generator[Session, Any, Any]:
    try:
        db = TestSessionLocal()
        yield db
    except Exception as e:
        db.rollback()
