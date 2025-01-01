import random
from datetime import datetime, timezone

import aiohttp
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    current_time = datetime.now(timezone.utc).isoformat()
    random_value = random.random()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://jsonplaceholder.typicode.com/users"
        ) as response:
            return {
                "time": current_time,
                "value": random_value,
                "status": response.status,
                "users": await response.json(),
            }
