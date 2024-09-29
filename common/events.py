from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from common.schemas import Coordinates, TaxiStatus


class ReportedForDutyEvent(BaseModel):
    event_type: Literal["reported-for-duty"] = "reported-for-duty"
    coordinates: Coordinates
    taxi_status: TaxiStatus


class RideRequestedEvent(BaseModel):
    event_type: Literal["ride-requested"] = "ride-requested"
    ride_id: UUID
    pick_up_coordinates: Coordinates
    drop_off_coordinates: Coordinates


class CustomerPickedUpEvent(BaseModel):
    event_type: Literal["customer-picked-up"] = "customer-picked-up"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ride_id: UUID
    coordinates: Coordinates


class CustomerDroppedOffEvent(BaseModel):
    event_type: Literal["customer-dropped-off"] = "customer-dropped-off"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ride_id: UUID
    coordinates: Coordinates


AnyEvent = Annotated[
    ReportedForDutyEvent | CustomerPickedUpEvent | CustomerDroppedOffEvent | RideRequestedEvent,
    Field(discriminator="event_type"),
]
