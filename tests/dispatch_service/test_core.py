from unittest.mock import Mock
from uuid import uuid4

import pytest
from starlette.websockets import WebSocketState

from common.schemas import Coordinates, TaxiStatus
from dispatch_service.core import Taxi


@pytest.mark.parametrize(
    ("taxi_status", "coordinates", "websocket_state", "expected_result"),
    [
        (TaxiStatus.AVAILABLE, Coordinates(), WebSocketState.CONNECTED, True),
        (TaxiStatus.AVAILABLE, None, WebSocketState.CONNECTED, False),
        (TaxiStatus.AVAILABLE, Coordinates(), WebSocketState.DISCONNECTED, False),
        (TaxiStatus.BUSY, Coordinates(), WebSocketState.CONNECTED, False),
        (TaxiStatus.BUSY, None, WebSocketState.DISCONNECTED, False),
    ],
)
def test_Taxi_can_accept_ride(
    taxi_status: TaxiStatus | None,
    coordinates: Coordinates | None,
    websocket_state: WebSocketState,
    expected_result: bool,
) -> None:
    # given
    taxi = Taxi(
        websocket=Mock(client_state=websocket_state), id=uuid4(), taxi_status=taxi_status, coordinates=coordinates
    )

    # when
    result = taxi.can_accept_ride

    # then
    assert result == expected_result
