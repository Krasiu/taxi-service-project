from uuid import UUID

from pydantic import BaseModel

from common.schemas import Coordinates


class RideRequestIn(BaseModel):
    user_id: UUID
    pick_up_coordinates: Coordinates
    drop_off_coordinates: Coordinates
