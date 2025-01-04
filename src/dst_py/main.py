import random
from datetime import datetime, timezone

import requests
from fastapi import FastAPI

from dst_py.database import Database

app = FastAPI()

database = Database()
database.create_db_and_tables()


@app.get("/users")
def read_users():
    current_time = datetime.now(timezone.utc).isoformat()
    random_value = random.random()
    response = requests.get("https://jsonplaceholder.typicode.com/users")

    return {
        "time": current_time,
        "random": random_value,
        "status": response.status_code,
        "users": response.json(),
    }


@app.get("/ping")
async def ping():
    return {"message": "PONG"}
