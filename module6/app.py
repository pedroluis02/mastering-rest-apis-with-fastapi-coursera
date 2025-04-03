import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from .commentrouter import commentRouter
from .database import database
from .postlikerouter import likeRouter
from .postrouter import postRouter
from .userrouter import userRouter

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("connect to database")
    await database.connect()
    yield
    logger.info("disconnect to database")
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(userRouter)
app.include_router(postRouter)
app.include_router(commentRouter)
app.include_router(likeRouter)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
