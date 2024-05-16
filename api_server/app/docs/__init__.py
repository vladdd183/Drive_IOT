"""
This module contains OpenAPI Documentation definition for the API.

It exposes a docs object that can be used to decorate request handlers with additional
information, used to generate OpenAPI documentation.
"""

from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import (
    Info,
    APIKeySecurity,
    HTTPSecurity,
    Security,
    SecurityRequirement,
    ParameterLocation
)

from app.settings import Settings


def configure_docs(app: Application, settings: Settings):
    docs = OpenAPIHandler(
        info=Info(title=settings.info.title, version=settings.info.version),
        anonymous_access=True,
        # security=Security([SecurityRequirement("bearer", [])]),
        security_schemes={
            "apiKeyAuth": APIKeySecurity(
                in_=ParameterLocation.HEADER,
                name="X-API-Key",
                description="API Key Auth",
            ),
            "BearerAuth": HTTPSecurity(scheme="bearer"),
        },
    )
    docs.security = Security([SecurityRequirement("apiKeyAuth", []),
                              SecurityRequirement("bearer", [])])
    # include only endpoints whose path starts with "/api/"
    docs.include = lambda path, _: path.startswith("/api/")
    docs.bind_app(app)
    return docs
