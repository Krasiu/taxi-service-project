import asyncio

import websockets
from loguru import logger
from websockets.asyncio.client import connect

from common.schemas import Coordinates, TaxiStatus
from common.utilities import configure_logging
from taxi_service.manager import DispatchConnectionManager
from taxi_service.settings import TAXI_SERVICE_SETTINGS


async def run() -> None:
    taxi_id = TAXI_SERVICE_SETTINGS.taxi_id
    taxi_client: DispatchConnectionManager | None = None
    async for websocket in connect(f"{TAXI_SERVICE_SETTINGS.dispatch_service_ws_url}/{taxi_id}"):
        taxi_client = DispatchConnectionManager(
            taxi_id=taxi_id,
            coordinates=Coordinates() if taxi_client is None else taxi_client.coordinates,
            status=TaxiStatus.AVAILABLE if taxi_client is None else taxi_client.status,
            websocket=websocket,
        )
        logger.info(
            f"Connecting to dispatch service with taxi id: {taxi_id}, coordinates: {taxi_client.coordinates}, status: {taxi_client.status}"
        )
        try:
            await taxi_client.connect_with_dispatch()
            await taxi_client.listen_for_events()
        except websockets.ConnectionClosed:
            continue


if __name__ == "__main__":
    configure_logging()
    asyncio.run(run())
