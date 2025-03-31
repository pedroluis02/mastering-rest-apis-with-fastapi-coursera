from pydantic import BaseModel

from .post import UserPost


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
