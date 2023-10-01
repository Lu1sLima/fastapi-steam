from fastapi import FastAPI
from database.database import create_db_and_tables
from routes.game_route import game_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(game_router)
