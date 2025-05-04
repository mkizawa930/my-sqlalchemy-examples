import factory

from sns import models
from .database import TestSessionLocal


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session_factory = TestSessionLocal
        sqlalchemy_session_persistence = "flush"

    nickname = "test user"
    email = "test@example.com"


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Post
        sqlalchemy_session_factory = TestSessionLocal
        sqlalchemy_session_persistence = "flush"

    title = "post title"
    body = "post body"
