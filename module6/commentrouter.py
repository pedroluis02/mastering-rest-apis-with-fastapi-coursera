from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .comment import Comment, CommentIn
from .database import database, comment_table
from .postrouter import find_post
from .security import get_current_user
from .user import User

commentRouter = APIRouter(prefix="/comments")


@commentRouter.post("", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
