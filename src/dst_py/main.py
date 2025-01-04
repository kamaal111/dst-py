from fastapi import FastAPI

from dst_py.auth.router import auth_router

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "PONG"}


app.include_router(auth_router)
