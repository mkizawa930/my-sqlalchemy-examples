from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from examples.sns.tests.conftest import db

from .models import CommentId, Post, PostId, PublicId, User, UserId, Comment


class UserCrud(object):
    def __init__(self):
        pass

    def create_user(self, db: Session, email: str, nickname: str) -> User:
        user = User(nickname=nickname, email=email)
        db.add(user)
        db.flush()
        return user

    def get_user_by_id(self, db: Session, user_id: UserId) -> User:
        return db.execute(select(User).where(User.id == user_id)).scalar_one()

    def get_user_by_public_id(self, db: Session, public_id: PublicId) -> User:
        return db.execute(select(User).where(User.public_id == public_id)).scalar_one()


class PostCrud(object):
    def create_post(self, db: Session, user_id: UserId, content: str):
        post = Post(user_id=user_id, content=content)
        db.add(post)
        db.flush()
        return post

    def get_post_by_id(self, db: Session, user_id: UserId, post_id: PostId) -> Post:
        stmt = (
            select(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.like_users),
            )
            .where(
                and_(
                    Post.id == post_id,
                    Post.user_id == user_id,
                )
            )
        )
        return db.execute(stmt).unique().scalar_one()

    def add_like_to_post(self, db: Session, user_id: UserId, post_id: PostId) -> Post:
        user = db.execute(select(User).where(User.id == user_id)).scalar_one()
        post = db.execute(select(Post).where(Post.id == post_id)).scalar_one()
        post.like_users.append(user)
        db.add(post)
        db.flush()
        return post


class CommentCrud(object):
    def __init__(self):
        pass

    def create_comment(
        self,
        db: Session,
        user_id: UserId,
        post_id: PostId,
        body: str,
    ) -> Comment:
        comment = Comment(user_id=user_id, post_id=post_id, body=body)
        db.add(comment)
        db.flush()
        return comment

    def get_comment_by_id(self, comment_id: CommentId) -> Comment:
        return db.execute(select(Comment).where(Comment.id == comment_id)).scalar_one()
