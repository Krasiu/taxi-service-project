from datetime import UTC, datetime
from typing import ClassVar
from uuid import UUID

from loguru import logger
from pydantic import TypeAdapter
from starlette.websockets import WebSocket

from common.events import (
    AnyEvent,
    CustomerDroppedOffEvent,
    CustomerPickedUpEvent,
    ReportedForDutyEvent,
    RideRequestedEvent,
)
from common.schemas import Coordinates, TaxiStatus
from common.utilities import calculate_manhattan_distance
from dispatch_service.core import Taxi
from dispatch_service.dal.operations import insert_new_ride, update_ride
from dispatch_service.dal.tables import rides
from dispatch_service.exceptions import NoTaxiAvailableError


class TaxiConnectionManager:
    fleet: ClassVar[dict[UUID, Taxi]] = {}
    AnyEventTA: TypeAdapter = TypeAdapter(AnyEvent)

    @classmethod
    async def connect(cls, websocket: WebSocket) -> None:
        await websocket.accept()
        taxi_id = UUID(websocket.path_params["taxi_id"])
        cls.fleet[taxi_id] = Taxi(id=taxi_id, websocket=websocket)

    @classmethod
    def disconnect(cls, taxi_id: UUID) -> None:
        cls.fleet.pop(taxi_id)

    @classmethod
    async def dispatch_taxi(
        cls, user_id: UUID, pick_up_coordinates: Coordinates, drop_off_coordinates: Coordinates
    ) -> None:
        now = datetime.now(tz=UTC)
        closest_taxi = cls._find_closest_taxi(pick_up_coordinates)
        if not closest_taxi:
            logger.warning("No taxis available")
            raise NoTaxiAvailableError

        ride_id = await insert_new_ride(
            user_id=user_id,
            taxi_id=closest_taxi.id,
            pick_up_coordinates=pick_up_coordinates,
            drop_off_coordinates=drop_off_coordinates,
            requested_at=now,
        )
        data = RideRequestedEvent(
            ride_id=ride_id,
            pick_up_coordinates=pick_up_coordinates,
            drop_off_coordinates=drop_off_coordinates,
        ).model_dump_json()
        await closest_taxi.websocket.send_text(data=data)
        closest_taxi.taxi_status = TaxiStatus.BUSY

    @classmethod
    async def handle_message(cls, text: str, taxi_id: UUID) -> None:
        taxi = cls.fleet[taxi_id]
        message = cls.AnyEventTA.validate_json(text)
        taxi.coordinates = message.coordinates

        if isinstance(message, ReportedForDutyEvent):
            logger.info(f"Taxi {taxi_id} is now reporting for duty at {message.coordinates}")
            taxi.taxi_status = message.taxi_status

        elif isinstance(message, CustomerPickedUpEvent):
            logger.info(f"Taxi {taxi_id} has picked up the customer at {message.coordinates}")
            await update_ride(
                ride_id=message.ride_id,
                values={rides.c.picked_up_at: message.timestamp},
            )
            taxi.taxi_status = TaxiStatus.BUSY

        elif isinstance(message, CustomerDroppedOffEvent):
            logger.info(f"Taxi {taxi_id} has dropped off the customer at {message.coordinates}")
            await update_ride(
                ride_id=message.ride_id,
                values={rides.c.dropped_off_at: message.timestamp},
            )
            taxi.taxi_status = TaxiStatus.AVAILABLE

        else:
            logger.warning(f"Unhandled message: {message}")

    @classmethod
    def _find_closest_taxi(cls, coordinates: Coordinates) -> Taxi | None:
        available_taxis = [taxi for taxi in cls.fleet.values() if taxi.can_accept_ride]
        if not available_taxis:
            return None

        return min(
            available_taxis,
            key=lambda taxi: calculate_manhattan_distance(taxi.coordinates, coordinates),
        )
