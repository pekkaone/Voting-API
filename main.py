from fastapi import FastAPI
from routers import Authentefication, Polls
from db.database import create_db_and_tables

app = FastAPI()

app.include_router(Authentefication.router, prefix="/authentefication", tags=["Auth"])
app.include_router(Polls.router, prefix="/poll", tags=["Polls"])