from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DispatchServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DISPATCH_SERVICE_")

    database_connection_string: str = "sqlite:///data/database.sqlite"

    @property
    def async_database_connection_string(self) -> str:
        return self.database_connection_string.replace("sqlite://", "sqlite+aiosqlite://")


@lru_cache(maxsize=1)
def get_dispatch_service_settings() -> DispatchServiceSettings:
    return DispatchServiceSettings()


DISPATCH_SERVICE_SETTINGS = get_dispatch_service_settings()
