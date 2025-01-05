from fastapi import FastAPI

from dst_py.auth.router import auth_router
from dst_py.health.router import health_router

app = FastAPI()


app.include_router(health_router)
app.include_router(auth_router)
