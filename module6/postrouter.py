from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .comment import Comment, UserPostWithComments
from .database import database, post_table, comment_table
from .post import UserPost, UserPostIn
from .security import get_current_user
from .user import User

postRouter = APIRouter(prefix="/posts")


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@postRouter.post("", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]):
    data = {**post.model_dump(), "user_id": current_user.id}
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@postRouter.get("", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@postRouter.get("/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }


@postRouter.get("/{post_id}/comments", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)
