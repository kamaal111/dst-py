from fastapi import FastAPI

from dst_py.auth.router import auth_router
from dst_py.database import Database

app = FastAPI()

database = Database()
database.create_db_and_tables()


@app.get("/ping")
async def ping():
    return {"message": "PONG"}


app.include_router(auth_router)
