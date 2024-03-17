from fastapi import FastAPI
from src.api import index

app = FastAPI()


app.include_router(index.index_router)
