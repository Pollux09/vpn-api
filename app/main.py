from fastapi import FastAPI

import requests
from deps import tokenDep

app = FastAPI()


@app.post("/create-user")
async def check(
   _: tokenDep
):
    return requests.create_user_request()
