from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .database import database, like_table
from .postlike import PostLike, PostLikeIn
from .postrouter import find_post
from .security import get_current_user
from .user import User

likeRouter = APIRouter(prefix="/likes")


@likeRouter.post("", response_model=PostLike, status_code=201)
async def like_post(
        like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**like.model_dump(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
