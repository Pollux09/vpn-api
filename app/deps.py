from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status
from starlette.requests import Request

from settings import settings


async def validate_token(request: Request):
    token = request.headers.get("App-token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    if token != settings.APP_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token


tokenDep = Annotated[str, Depends(validate_token)]
