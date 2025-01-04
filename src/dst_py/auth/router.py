import random
from datetime import datetime, timezone

import requests
from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import EmailStr, ValidationError
from sqlmodel import Session

from dst_py.database import Database, get_database

from .models import User
from .schemas import UserSchema

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
    try:
        validated_payload = UserSchema(email=email, password=password)
    except ValidationError as e:
        raise HTTPException(400, e.errors()) from e

    with Session(database.engine) as session:
        user = User.create(payload=validated_payload, session=session)

        return {"email": user.email}
