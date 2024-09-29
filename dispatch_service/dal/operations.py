import uuid
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Column, insert, update

from common.schemas import Coordinates
from dispatch_service.dal.database import database
from dispatch_service.dal.tables import rides


async def insert_new_ride(
    taxi_id: UUID,
    user_id: UUID,
    pick_up_coordinates: Coordinates,
    drop_off_coordinates: Coordinates,
    requested_at: datetime | None = None,
) -> UUID:
    query = (
        insert(rides)
        .values(
            {
                rides.c.id: uuid.uuid4(),
                rides.c.taxi_id: taxi_id,
                rides.c.user_id: user_id,
                rides.c.requested_at: requested_at or datetime.now(tz=UTC),
                rides.c.pick_up_coordinates: pick_up_coordinates.model_dump(),
                rides.c.drop_off_coordinates: drop_off_coordinates.model_dump(),
            }
        )
        .returning(rides.c.id)
    )
    return await database.fetch_val(query=query)


async def update_ride(ride_id: UUID, values: dict[Column, Any]) -> None:
    query = update(rides).where(rides.c.id == ride_id).values(values)
    await database.execute(query=query)
