import asyncio
from datetime import timedelta
from uuid import uuid4

from aiohttp import ClientSession
from loguru import logger

from common.schemas import Coordinates
from common.utilities import configure_logging
from ride_requester_service.settings import RIDE_REQUESTER_SERVICE_SETTINGS

TASKS: set[asyncio.Task] = set()


async def post_ride_request(pick_up_coordinates: Coordinates, drop_off_coordinates: Coordinates) -> None:
    async with ClientSession() as session:
        response = await session.post(
            f"{RIDE_REQUESTER_SERVICE_SETTINGS.dispatch_service_api_base_url}/ride-request",
            json={
                "user_id": str(uuid4()),
                "pick_up_coordinates": pick_up_coordinates.model_dump(),
                "drop_off_coordinates": drop_off_coordinates.model_dump(),
            },
        )
    if not response.ok:
        logger.warning("Failed to request ride")
        return

    logger.info("Ride requested successfully")


async def request_rides(interval: timedelta, number_of_rides: int) -> None:
    while True:
        for _ in range(number_of_rides):
            pick_up_coordinates = Coordinates()
            drop_off_coordinates = Coordinates()
            logger.info(
                f"Requesting ride with pick up coordinates: {pick_up_coordinates} and drop off coordinates: {drop_off_coordinates}"
            )
            task = asyncio.create_task(
                post_ride_request(
                    pick_up_coordinates=pick_up_coordinates,
                    drop_off_coordinates=drop_off_coordinates,
                )
            )
            TASKS.add(task)
            task.add_done_callback(TASKS.remove)

        await asyncio.sleep(interval.total_seconds())


if __name__ == "__main__":
    configure_logging()
    asyncio.run(
        request_rides(
            interval=timedelta(seconds=RIDE_REQUESTER_SERVICE_SETTINGS.interval_seconds),
            number_of_rides=RIDE_REQUESTER_SERVICE_SETTINGS.number_of_rides,
        )
    )
