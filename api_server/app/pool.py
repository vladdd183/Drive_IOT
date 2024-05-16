from piccolo.engine import engine_finder
from blacksheep.server import Application


def configure_pool_control(app: Application):
    async def open_database_connection_pool(app: Application):
        try:
            engine = engine_finder()
            await engine.start_connection_pool()
        except Exception:
            print("Unable to connect to the database")

    async def close_database_connection_pool(app: Application):
        try:
            engine = engine_finder()
            await engine.close_connection_pool()
        except Exception as e:
            print(f"Unable to connect to postgres: {e}")

    app.on_start += open_database_connection_pool
    app.on_stop += close_database_connection_pool
