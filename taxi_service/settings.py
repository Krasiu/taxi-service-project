import uuid
from functools import lru_cache
from uuid import UUID

from pydantic import Field, WebsocketUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class TaxiServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TAXI_SERVICE_")

    dispatch_service_ws_url: WebsocketUrl = "ws://dispatch_service:8000/ws"
    taxi_id: UUID = Field(default_factory=uuid.uuid4)


@lru_cache(maxsize=1)
def get_taxi_service_settings() -> TaxiServiceSettings:
    return TaxiServiceSettings()


TAXI_SERVICE_SETTINGS = get_taxi_service_settings()
