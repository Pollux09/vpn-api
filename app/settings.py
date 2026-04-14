from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: HttpUrl
    CREATE_USER_PATH: str
    API_TOKEN: str

    APP_TOKEN: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

settings = Settings()