from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    BOT_TOKEN: str = ""
    WEBHOOK_URL: str = ""
    WEBAPP_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env",
        extra="forbid",
        env_file_encoding="utf-8",
    )


def get_settings():
    return Settings()
