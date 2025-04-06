from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseResourceSettings(BaseSettings):
    PORT: str | None = None
    HOST: str = "localhost"
    SECURE: bool = False

    @property
    def PROTOCOL(self) -> str:
        return "https" if self.SECURE else "http"

    @property
    def url(self) -> str:
        return f"{self.PROTOCOL}://{self.HOST}{":" + self.PORT if self.PORT else ""}"


class MINIAPPSettings(BaseResourceSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
        env_prefix="MINIAPP_",
    )


class APISettings(BaseResourceSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
        env_prefix="API_",
    )


class WEBSettings(BaseResourceSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
        env_prefix="WEB_",
    )


class Settings(BaseSettings):
    DEBUG: bool = False

    BOT_TOKEN: str = ""
    BOT_PORT: int = 8001
    BOT_HOST: str = "localhost"
    BOT_SECRET: str = "somesecret"

    MINIAPP: MINIAPPSettings = MINIAPPSettings()
    API: APISettings = APISettings()
    WEB: WEBSettings = WEBSettings()

    WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


def get_settings():
    return Settings()
