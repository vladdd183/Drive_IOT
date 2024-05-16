"""
This module configures the BlackSheep application before it starts.
"""
from blacksheep import Application
from rodi import Container

from app.auth import configure_authentication
from app.docs import configure_docs
from app.errors import configure_error_handlers
from app.services import configure_services
from app.routers import configure_routers
from app.pool import configure_pool_control
from app.cors import configure_cors
from app.settings import load_settings, Settings

from blacksheep.server.headers.cache import CacheControlMiddleware


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    app.middlewares.append(CacheControlMiddleware(no_cache=True, no_store=True))
    configure_error_handlers(app)
    configure_authentication(app)
    configure_cors(app)
    docs = configure_docs(app, settings)
    configure_routers(app, docs)
    configure_pool_control(app)
    app.serve_files(
    "app/static",
    index_document="index.html")
    return app


app = configure_application(*configure_services(load_settings()))
