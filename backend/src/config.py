from functools import cache

from pydantic_settings import BaseSettings


@cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    # Define your settings here
    app_name: str = "Feather"
