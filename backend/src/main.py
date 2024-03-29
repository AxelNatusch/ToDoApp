from fastapi import FastAPI

from src.api import index
from src.api.todo import basic_todo as todo_router

app = FastAPI()


app.include_router(index.index_router)
app.include_router(todo_router.router)
