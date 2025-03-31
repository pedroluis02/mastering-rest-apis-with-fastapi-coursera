from fastapi import FastAPI

from module2.router import postRouter, commentRouter

app = FastAPI()
app.include_router(postRouter)
app.include_router(commentRouter)

if __name__ == '__main__':
    print('Mastering REST APIs with FastAPI - Coursera')
