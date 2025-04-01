from fastapi import FastAPI

from module2.router import postRouter, commentRouter

app = FastAPI()
app.include_router(postRouter)
app.include_router(commentRouter)
