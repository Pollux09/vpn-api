from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=36, pattern=r"^[a-zA-Z0-9_-]+$")
    days: int = Field(ge=1)
    status: Literal["ACTIVE", "DISABLED", "LIMITED", "EXPIRED"] = "ACTIVE"
    traffic_limit_bytes: int = Field(default=53_687_091_200, ge=0)
    traffic_limit_strategy: Literal["NO_RESET", "DAY", "WEEK", "MONTH"] = "MONTH"


class CreateUserResponse(BaseModel):
    subscription_url: HttpUrl


class PanelCreateUserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    uuid: str
    username: str

    vlessUuid: Optional[str] = None
    trojanPassword: Optional[str] = None
    ssPassword: Optional[str] = None

    shortUuid: Optional[str] = None
    subscriptionUrl: Optional[HttpUrl] = None

    expireAt: datetime
    trafficLimitBytes: Optional[int] = None


class PanelCreateUserEnvelope(BaseModel):
    response: PanelCreateUserResponse
