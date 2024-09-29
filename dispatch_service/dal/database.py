from databases import Database

from dispatch_service.settings import DISPATCH_SERVICE_SETTINGS

database = Database(DISPATCH_SERVICE_SETTINGS.async_database_connection_string)
