import random
from datetime import datetime, timezone

import requests
from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/users")
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


# @auth_router.post("/register")
# def register(): ...
