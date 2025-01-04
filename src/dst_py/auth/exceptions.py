from typing import Dict

from fastapi import HTTPException


class UserAlreadyExists(HTTPException):
    def __init__(self, headers: Dict[str, str] | None = None) -> None:
        super().__init__(409, "User already exists", headers)
