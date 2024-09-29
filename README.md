# Taxi Service Project

This project consists of multiple services to manage a taxi dispatch system. The services are built using Python and Docker, and they communicate with each other via HTTP and WebSocket.

## Services

1. **Dispatch Service**: Manages ride requests and dispatches taxis.
2. **Taxi Service**: Simulates taxis that communicate with the dispatch service.
3. **Ride Requester Service**: Simulates users requesting rides.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Krasiu/taxi-service-project.git
    cd taxi-service-project
    ```

2. Create a `.env` file based on the `.env.example`:
    ```sh
    cp .env.example .env
    ```

3. Update the `.env` file with your configuration.

## Building and Running the Services

1. Build and start the services using Docker Compose:
    ```sh
    docker-compose up --build
    ```

## Health Checks

- The `dispatch_service` has a health check configured to ensure it is running correctly.

## Configuration

- The services can be configured using environment variables defined in the `.env` file.
