import httpx
from fastapi import HTTPException

from settings import settings


async def create_user_request():
    try:
        url = settings.BASE_URL + settings.CREATE_USER_PATH
        result = httpx.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": settings.API_KEY,
            }
        )
        #result logics
    except:
        raise HTTPException(status_code=500, detail="API error")