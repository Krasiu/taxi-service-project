import asyncio
import random
import uuid

from loguru import logger
from pydantic import ValidationError
from websockets.asyncio.client import ClientConnection

from common.events import (
    CustomerDroppedOffEvent,
    CustomerPickedUpEvent,
    ReportedForDutyEvent,
    RideRequestedEvent,
)
from common.schemas import Coordinates, TaxiStatus
from common.utilities import calculate_manhattan_distance


class DispatchConnectionManager:
    def __init__(
        self,
        taxi_id: uuid.UUID,
        coordinates: Coordinates,
        status: TaxiStatus,
        websocket: ClientConnection,
    ) -> None:
        self.taxi_id = taxi_id
        self.coordinates = coordinates
        self.status = status
        self.websocket = websocket
        self._task: asyncio.Task | None = None

    async def connect_with_dispatch(self) -> None:
        report_for_duty_event = ReportedForDutyEvent(coordinates=self.coordinates, taxi_status=self.status)
        await self.websocket.send(report_for_duty_event.model_dump_json())

    async def listen_for_events(self) -> None:
        async for websocket_message in self.websocket:
            if self.status == TaxiStatus.BUSY:
                continue

            try:
                ride_requested_event = RideRequestedEvent.model_validate_json(websocket_message)
            except ValidationError:
                logger.warning(f"Received invalid message: {websocket_message}")
                continue

            await self.handle_ride_request(ride_requested_event)

    async def handle_ride_request(self, event: RideRequestedEvent) -> None:
        logger.info(f"Received ride request: {event}, changing status to BUSY")
        self.status = TaxiStatus.BUSY
        await self._pick_up_customer(ride_id=event.ride_id, pick_up_coordinates=event.pick_up_coordinates)
        await self._drop_off_customer(event.ride_id, event.drop_off_coordinates)
        self.status = TaxiStatus.AVAILABLE

    async def _pick_up_customer(self, ride_id: uuid.UUID, pick_up_coordinates: Coordinates) -> None:
        await self._drive(to_coordinates=pick_up_coordinates)
        logger.info(f"Picked up customer at {pick_up_coordinates}")
        await self.websocket.send(
            CustomerPickedUpEvent(ride_id=ride_id, coordinates=pick_up_coordinates).model_dump_json()
        )
        self.coordinates = pick_up_coordinates

    async def _drop_off_customer(self, ride_id: uuid.UUID, drop_off_coordinates: Coordinates) -> None:
        await self._drive(to_coordinates=drop_off_coordinates)
        logger.info(f"Dropped off customer at {drop_off_coordinates}")
        await self.websocket.send(
            CustomerDroppedOffEvent(ride_id=ride_id, coordinates=drop_off_coordinates).model_dump_json()
        )
        self.coordinates = drop_off_coordinates

    async def _drive(self, to_coordinates: Coordinates) -> None:
        logger.info(f"Driving from {self.coordinates} to {to_coordinates}")
        for _ in range(calculate_manhattan_distance(self.coordinates, to_coordinates)):
            await asyncio.sleep(random.uniform(1, 3))
