from utils.constants import (
    DATABASE_CONFIG
)
import os

def load_database_params():
    port = os.getenv("DB_PORT", DATABASE_CONFIG["DB_PORT"])
    port = int(port)

    params = {
        "host": os.getenv("DB_HOST", DATABASE_CONFIG["DB_HOST"]),
        "port": port,
        "username": os.getenv("DB_USERNAME", DATABASE_CONFIG["DB_USERNAME"]),
        "password": os.getenv("DB_PASSWORD", DATABASE_CONFIG["DB_PASSWORD"]),
        "authSource": os.getenv("authSource", DATABASE_CONFIG["authSource"]),
        "authMechanism": os.getenv("authMechanism", DATABASE_CONFIG["authMechanism"])
    }

    return params