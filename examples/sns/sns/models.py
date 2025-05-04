from datetime import date, datetime
from typing import List
from uuid import uuid4
from sqlalchemy import (
    UUID,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import func


from .database import Base

UserId = int
PublicId = UUID
PostId = int
CommentId = int


class TimestampMixin(object):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(Integer, primary_key=True)
    public_id: Mapped[UUID] = mapped_column(String, nullable=False, default=uuid4().hex, server_default=func.uuid())
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=None)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    # 関連オブジェクトを経由する場合はsecondaryのみでよい
    like_posts: Mapped[List["Post"]] = relationship(
        "Post",
        secondary="user_post_likes",
        back_populates="like_users",
    )


# user_associations = Table(
#     "user_associations",
#     Base.metadata,
#     Column("follower_id", ForeignKey("users.id"), comment="フォローする人"),
#     Column("followee_id", ForeignKey("users.id"), comment="フォローされる人"),
# )


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=None)
    user: Mapped[User] = relationship(back_populates="posts")

    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    like_users: Mapped[List["User"]] = relationship(secondary="user_post_likes", back_populates="like_posts")


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[CommentId] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[PostId] = mapped_column(ForeignKey("posts.id"))
    body: Mapped[str] = mapped_column(Text)

    user: Mapped[User] = relationship(User, back_populates="comments")
    post: Mapped[Post] = relationship(Post, back_populates="comments")


class UserPostLike(Base, TimestampMixin):
    __tablename__ = "user_post_likes"

    user_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"), primary_key=True)
    post_id: Mapped[PostId] = mapped_column(ForeignKey("posts.id"), primary_key=True)
