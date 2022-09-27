import enum
import os
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


# class LogLevel(str, enum.Enum):  # noqa: WPS600
#     """Possible log levels."""

#     NOTSET = "NOTSET"
#     DEBUG = "DEBUG"
#     INFO = "INFO"
#     WARNING = "WARNING"
#     ERROR = "ERROR"
#     FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    project_name: str = os.getenv("PROJECT_NAME", "lira-map-fastapi")
    project_version: str = os.getenv("PROJECT_VERSION", "0.0.1")
    host: str = os.getenv("API_HOST_IP", "127.0.0.1")
    port: int = int(os.getenv("API_PORT", 8000))
    # quantity of workers for uvicorn
    workers_count: int = int(os.getenv("WORKERS_COUNT", 1))
    # Enable uvicorn reloading
    # This is a terrible way to do this parsing
    reload: bool = bool(os.getenv("RELOAD_API", False))

    # Current environment
    environment: str = os.getenv("DEPLOY_ENVIRONMENT", "dev")

    # log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    # This needs to also look at the .env file to configure and get the values from that.
    # You could make the case that this file could be used for configs, but no, it should only
    # Be used for reading the env file as a back up if it is not provided explicitly in this file.
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_user: str = os.getenv("DB_USER", "lira_backend_api")
    db_pass: str = os.getenv("DB_PASS", "lira_backend_api")
    db_base: str = os.getenv("DB_BASE", "lira_backend_api")
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
            # scheme="postgresql+asyncpg",
        )

    class Config:
        env_file = ".env"
        # WTF is this doing?
        # env_prefix = "LIRA_BACKEND_API_"
        env_file_encoding = "utf-8"


settings = Settings()
