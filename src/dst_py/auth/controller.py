import random
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

import jwt
import requests
from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlmodel import Session

from dst_py.conf import settings
from dst_py.database import BaseDatabase, get_database

from .exceptions import InvalidCredentials
from .models import User
from .schemas import LoginResponse, UserSchema


class AuthController:
    database: BaseDatabase

    def __init__(self, database: BaseDatabase) -> None:
        self.database = database

    def register(self, email: str, password: str):
        try:
            validated_payload = UserSchema(email=email, password=password)
        except ValidationError as e:
            raise HTTPException(HTTPStatus.BAD_REQUEST, e.errors()) from e

        with Session(self.database.engine) as session:
            User.create(payload=validated_payload, session=session)

            return {"details": "Created"}

    def login(self, email: str, password: str):
        try:
            validated_payload = UserSchema(email=email, password=password)
        except ValidationError as e:
            raise HTTPException(HTTPStatus.BAD_REQUEST, e.errors()) from e

        with Session(self.database.engine) as session:
            user = User.get_by_email(email=validated_payload.email, session=session)
            if user is None:
                raise InvalidCredentials

        if not user.verify_password(raw_password=validated_payload.password):
            raise InvalidCredentials

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expire_minutes
        )
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


def get_auth_controller(database: Annotated[BaseDatabase, Depends(get_database)]):
    controller = AuthController(database=database)
    yield controller
