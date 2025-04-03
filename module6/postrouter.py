from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException

from .comment import Comment
from .database import database, post_table, comment_table, like_table
from .post import UserPost, UserPostIn, UserPostWithComments, UserPostWithLikes
from .postsort import UserPostSorting
from .security import get_current_user
from .user import User

postRouter = APIRouter(prefix="/posts")

select_post_and_likes = (
    sqlalchemy.select(post_table, sqlalchemy.func.count(like_table.c.id).label("likes"))
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@postRouter.post("", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]):
    data = {**post.model_dump(), "user_id": current_user.id}
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@postRouter.get("", response_model=list[UserPostWithLikes])
async def get_all_posts():
    query = select_post_and_likes
    return await database.fetch_all(query)


@postRouter.get("/sorting", response_model=list[UserPostWithLikes])
async def get_all_posts_with_sorting(sorting: UserPostSorting = UserPostSorting.new):
    if sorting == UserPostSorting.new:
        query = select_post_and_likes.order_by(post_table.c.id.desc())
    elif sorting == UserPostSorting.old:
        query = select_post_and_likes.order_by(post_table.c.id.asc())
    elif sorting == UserPostSorting.most_likes:
        query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))

    return await database.fetch_all(query)


@postRouter.get("/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    query = select_post_and_likes.where(post_table.c.id == post_id)
    post = await database.fetch_one(query)
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
