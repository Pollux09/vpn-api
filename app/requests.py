from datetime import datetime, timezone, timedelta

import httpx
from fastapi import HTTPException

from schemas.schemas import PanelCreateUserEnvelope, PanelCreateUserResponse, PanelInternalSquadsEnvelope
from settings import settings


async def create_user_request(
    username: str,
    days: int,
    internal_squads_ids: list[str],
    status: str = "ACTIVE",
    traffic_limit_bytes: int = 53687091200,
    traffic_limit_strategy: str = "MONTH",
) -> PanelCreateUserResponse:
    base_url = str(settings.BASE_URL).rstrip("/")
    path = settings.CREATE_USER_PATH.lstrip("/")
    url = f"{base_url}/{path}"
    headers = {
        "Authorization": f"Bearer {settings.API_TOKEN}",
        "Content-Type": "application/json",
    }

    if settings.API_KEY:
        headers["X-Api-Key"] = settings.API_KEY

    payload = {
        "username": username,
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=days)).isoformat(),
        "status": status,
        "trafficLimitBytes": traffic_limit_bytes,
        "trafficLimitStrategy": traffic_limit_strategy,
        "activeInternalSquads": [internal_squads_ids[0]],
    }

    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            result = await client.post(url=url, headers=headers, json=payload)
            result.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text or "Remnawave API returned an error"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Remnawave API is unavailable") from exc

    try:
        response = PanelCreateUserEnvelope.model_validate(result.json())
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unexpected Remnawave API response") from exc

    return response.response


async def get_internal_squads_ids() -> list[str]:
    base_url = str(settings.BASE_URL).rstrip("/")
    path = settings.INTERNAL_SQUADS_PATH.lstrip("/")
    url = f"{base_url}/{path}"

    headers = {
        "Authorization": f"Bearer {settings.API_TOKEN}",
        "Content-Type": "application/json",
    }

    if settings.API_KEY:
        headers["X-Api-Key"] = settings.API_KEY

    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            result = await client.get(url=url, headers=headers)
            result.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text or "Remnawave API returned an error"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Remnawave API is unavailable") from exc

    try:
        data = PanelInternalSquadsEnvelope.model_validate(result.json())
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unexpected Remnawave API response") from exc

    uuids = [s.uuid for s in data.response.internalSquads]
    return uuids
