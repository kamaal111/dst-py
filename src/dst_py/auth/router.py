from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr

from .controller import AuthControllable, get_auth_controller
from .schemas import LoginResponse, RegisterResponse

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", status_code=HTTPStatus.CREATED)
def register(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    controller: Annotated[AuthControllable, Depends(get_auth_controller)],
) -> RegisterResponse:
    return controller.register(email=email, password=password)


@auth_router.post("/login", status_code=HTTPStatus.OK)
def login(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    controller: Annotated[AuthControllable, Depends(get_auth_controller)],
) -> LoginResponse:
    return controller.login(email=email, password=password)
