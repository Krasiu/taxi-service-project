from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from common.schemas import Coordinates
from dispatch_service.dal.database import database
from dispatch_service.dal.operations import insert_new_ride, update_ride
from dispatch_service.dal.tables import rides


@pytest.mark.component
async def test_insert_new_ride() -> None:
    # when
    ride_id = await insert_new_ride(
        taxi_id=uuid4(), user_id=uuid4(), pick_up_coordinates=Coordinates(), drop_off_coordinates=Coordinates()
    )

    # then
    assert isinstance(ride_id, UUID)


@pytest.mark.component
async def test_update_ride() -> None:
    # given
    ride_id = await insert_new_ride(
        taxi_id=uuid4(), user_id=uuid4(), pick_up_coordinates=Coordinates(), drop_off_coordinates=Coordinates()
    )
    picked_up_at = datetime.now(tz=UTC)

    # when
    await update_ride(ride_id, {rides.c.picked_up_at: picked_up_at})
    record = await database.fetch_one(select(rides).where(rides.c.id == ride_id))

    # then
    assert record[rides.c.picked_up_at].time() == picked_up_at.time()
    assert record[rides.c.picked_up_at].date() == picked_up_at.date()
