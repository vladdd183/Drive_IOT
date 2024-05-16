from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry
import os


DB = PostgresEngine(
    config={
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
    }
)

APP_REGISTRY = AppRegistry(
    apps=["app.piccoloModule.piccolo_app", "piccolo_admin.piccolo_app"]
)
