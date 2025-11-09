from pydantic_settings import BaseSettings, SettingsConfigDict
import os

_base_config = SettingsConfigDict(
    env_file="../env", env_ignore_empty=True, extra="ignore"
)


class DatataseSettings(BaseSettings):
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "herfa-ecommerce"
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "password.1"
