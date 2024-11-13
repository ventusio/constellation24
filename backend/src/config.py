from functools import cache
from uuid import uuid4

from pydantic_settings import BaseSettings, SettingsConfigDict


@cache
def get_settings():
    print("settings =", Settings().model_dump_json(indent=2))
    return Settings()


class Settings(BaseSettings):
    app_name: str = "Feather"
    db_user: str = "postgres"
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    admin_key: str = str(uuid4())

    model_config = SettingsConfigDict(env_file=".env")
