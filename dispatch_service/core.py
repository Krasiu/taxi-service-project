from uuid import UUID, uuid4

from starlette.websockets import WebSocket, WebSocketState

from common.schemas import Coordinates, TaxiStatus


class Taxi:
    def __init__(
        self,
        websocket: WebSocket,
        id: UUID | None = None,
        taxi_status: TaxiStatus = None,
        coordinates: Coordinates = None,
    ) -> None:
        self.id = id or uuid4()
        self.websocket = websocket
        self.taxi_status = taxi_status
        self.coordinates = coordinates

    @property
    def can_accept_ride(self) -> bool:
        return bool(
            self.taxi_status == TaxiStatus.AVAILABLE
            and self.coordinates
            and self.websocket.client_state == WebSocketState.CONNECTED
        )
