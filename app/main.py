from fastapi import FastAPI, HTTPException
from starlette import status

import requests
from deps import tokenDep
from schemas.schemas import CreateUserRequest, CreateUserResponse

app = FastAPI()


@app.post("/create-user")
async def create_user(
    _: tokenDep,
    create_user_data: CreateUserRequest
) -> CreateUserResponse:
    result = await requests.create_user_request(
        username=create_user_data.username,
        days=create_user_data.days,
        status=create_user_data.status,
        traffic_limit_bytes=create_user_data.traffic_limit_bytes,
        traffic_limit_strategy=create_user_data.traffic_limit_strategy,
    )

    if not result.subscriptionUrl:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Remnawave did not return a subscription URL",
        )

    return CreateUserResponse(subscription_url=result.subscriptionUrl)
