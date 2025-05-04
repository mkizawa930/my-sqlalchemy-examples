from typing import Generator
import pytest
from sqlalchemy.orm import Session

from sns.crud import PostCrud, UserCrud
from tests.factories import PostFactory, UserFactory


@pytest.fixture(scope="function")
def user_crud() -> Generator[UserCrud, None, None]:
    return UserCrud()


@pytest.fixture(scope="function")
def post_crud() -> Generator[PostCrud, None, None]:
    return PostCrud()


class TestUserCrud:
    @pytest.mark.parametrize(
        "email,nickname",
        [
            ("user@example.com", "test user"),
        ],
    )
    def test_ユーザー登録(self, db: Session, user_crud: UserCrud, email, nickname):
        user = user_crud.create_user(db, email, nickname)
        assert user.id > 0


class Test_PostCrud:
    def test_投稿を取得する(self, db: Session, post_crud: PostCrud):
        user1 = UserFactory(email="user1@example.com", nickname="user1")
        user2 = UserFactory(email="user2@example.com", nickname="user2")

        want = PostFactory(user=user1, like_users=[user2])

        got = post_crud.get_post_by_id(db, user_id=user1.id, post_id=want.id)

        assert got
        assert got.id > 0
        assert got.user_id == user1.id

    def test_投稿にいいねする(self, db: Session, post_crud: PostCrud):
        user = UserFactory()
        post = PostFactory(user_id=user.id)
        post_crud.add_like_to_post(db, user.id, post.id)
