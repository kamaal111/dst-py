import random
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
import requests
from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import EmailStr, ValidationError
from sqlmodel import Session

from dst_py.conf import settings
from dst_py.database import Database, get_database

from .exceptions import InvalidCredentials
from .models import User
from .schemas import LoginResponse, UserSchema

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


@auth_router.post("/register", status_code=HTTPStatus.CREATED)
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


@auth_router.post("/login", status_code=HTTPStatus.OK)
def login(
    email: EmailStr = Form(),
    password: str = Form(),
    database: Database = Depends(get_database),
) -> LoginResponse:
    try:
        validated_payload = UserSchema(email=email, password=password)
    except ValidationError as e:
        raise HTTPException(400, e.errors()) from e

    with Session(database.engine) as session:
        user = User.get_by_email(email=validated_payload.email, session=session)
        if user is None:
            raise InvalidCredentials()

    if not user.verify_password(raw_password=validated_payload.password):
        raise InvalidCredentials()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    access_token = jwt.encode(
        {"sub": user.id, "exp": expire},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    random_value = random.random()
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status()

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        random=random_value,
        external_data=response.json(),
    )
