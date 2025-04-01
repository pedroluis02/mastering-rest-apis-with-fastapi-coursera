from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import database
from .router import postRouter, commentRouter


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(postRouter)
app.include_router(commentRouter)
