from sqlalchemy import create_engine

from dispatch_service.dal.tables import metadata
from dispatch_service.settings import DISPATCH_SERVICE_SETTINGS


def create_tables() -> None:
    metadata.create_all(create_engine(DISPATCH_SERVICE_SETTINGS.database_connection_string))


if __name__ == "__main__":
    create_tables()
