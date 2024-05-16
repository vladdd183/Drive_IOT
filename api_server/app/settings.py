"""
Application settings handled using Pydantic Settings management.

Pydantic is used both to read app settings from various sources, and to validate their
values.

https://docs.pydantic.dev/latest/usage/settings/
"""
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ


class APIInfo(BaseModel):
    title: str = "Auth API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Settings(BaseSettings):
    info: APIInfo = APIInfo()
    app: App = App()
    model_config = SettingsConfigDict(env_prefix="APP_")


def load_settings() -> Settings:
    return Settings()
