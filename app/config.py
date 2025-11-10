from pydantic_settings import BaseSettings, SettingsConfigDict
import os

_base_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)

"""_summary_
    Database Settings
"""


class DatataseSettings(BaseSettings):
    def __int__(self):
        from app.utils import logging_service, LogType, LogServiceType

        # log whenever DatabaseSetting is called
        logging_service.set_log(
            message="Database Settings was used",
            service_type=LogServiceType.DATABASE,
            log_type=LogType.INFO,
        )

    # postgres .env details
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST") or ""
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT") or 0)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB") or ""
    POSTGRES_USER: str = os.getenv("POSTGRES_USER") or ""
    POSTGRES_PASS: str = os.getenv("POSTGRES_PASS") or ""

    # redis .env details
    REDIS_SERVER: str = os.getenv("REDIS_SERVER") or ""
    REDIS_PORT: int = int(os.getenv("REDIS_PORT") or 0)

    model_config = _base_config

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# instantiate DatabaseSetting()
database_settings = DatataseSettings()

"""_summary_
    Security Settings
"""


class SecuritySettings(BaseSettings):
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM") or ""
    JWT_SECRET: str = os.getenv("JWT_SECRET") or ""
    model_config = _base_config


# instantiate SecuritySettings()
security_settings = SecuritySettings()
