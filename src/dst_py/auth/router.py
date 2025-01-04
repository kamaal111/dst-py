import random
from datetime import datetime, timezone

import requests
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from sqlmodel import Session

from dst_py.database import Database, get_database

from .models import User

auth_router = APIRouter(prefix="/auth")


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


@auth_router.post("/register")
def register(
    email: EmailStr = Form(),
    password: str = Form(),
    database: Database = Depends(get_database),
):
    with Session(database.engine) as session:
        user = User.create(email=email, raw_password=password, session=session)

        return {"email": user.email}
