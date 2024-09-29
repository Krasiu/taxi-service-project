from functools import lru_cache

from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class RideRequesterServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RIDE_REQUESTER_SERVICE_")

    dispatch_service_api_base_url: Url = "http://dispatch_service:8000/api"
    interval_seconds: int = 30
    number_of_rides: int = 2


@lru_cache(maxsize=1)
def get_ride_requester_service_settings() -> RideRequesterServiceSettings:
    return RideRequesterServiceSettings()


RIDE_REQUESTER_SERVICE_SETTINGS = get_ride_requester_service_settings()
