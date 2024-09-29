from contextlib import asynccontextmanager
from typing import Generator
from uuid import UUID

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from starlette import status

from common.utilities import configure_logging
from dispatch_service.dal.database import database
from dispatch_service.exceptions import NoTaxiAvailableError
from dispatch_service.manager import TaxiConnectionManager
from dispatch_service.schemas import RideRequestIn


@asynccontextmanager
async def lifespan(_: FastAPI) -> Generator[None, None, None]:
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/api/ride-request")
async def post_ride_request(ride_request_in: RideRequestIn) -> Response:
    try:
        await TaxiConnectionManager.dispatch_taxi(
            user_id=ride_request_in.user_id,
            pick_up_coordinates=ride_request_in.pick_up_coordinates,
            drop_off_coordinates=ride_request_in.drop_off_coordinates,
        )
    except NoTaxiAvailableError:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.websocket("/ws/{taxi_id}")
async def websocket_endpoint(websocket: WebSocket, taxi_id: UUID) -> None:
    await TaxiConnectionManager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            await TaxiConnectionManager.handle_message(text=text, taxi_id=taxi_id)
    except WebSocketDisconnect:
        TaxiConnectionManager.disconnect(taxi_id)
