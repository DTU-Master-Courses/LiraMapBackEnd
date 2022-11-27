import os
from pathlib import Path
from tempfile import gettempdir
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    project_name: str = os.getenv("PROJECT_NAME", "lira_backend_api")
    project_version: str = os.getenv("PROJECT_VERSION", "0.0.1")
    host: str = os.getenv("API_HOST_IP", "127.0.0.1")
    port: int = int(os.getenv("API_PORT", 8000))
    # quantity of workers for uvicorn
    workers_count: int = int(os.getenv("WORKERS_COUNT", 1))
    # Enable uvicorn reloading
    reload: bool = bool(os.getenv("RELOAD_API", False))

    # Current environment
    environment: str = os.getenv("DEPLOY_ENVIRONMENT", "dev")

    # Variables for the database
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_user: str = os.getenv("DB_USER", "lira_backend_api")
    db_pass: str = os.getenv("DB_PASS", "lira_backend_api")
    db_base: str = os.getenv("DB_BASE", "lira_backend_api")
    db_echo: bool = False

    # This comes from Azure environment
    altitude_db_host: str = os.getenv("ALTITUDE_DB_HOST", "localhost")
    altitude_db_port: int = int(os.getenv("ALTITUDE_DB_PORT", 5432))
    altitude_db_user: str = os.getenv("ALTITUDE_DB_USER", "lira_backend_api")
    altitude_db_pass: str = os.getenv("ALTITUDE_DB_PASS", "lira_backend_api")
    altitude_db_base: str = os.getenv("ALTITUDE_DB_BASE", "lira_backend_api")

    # @property
    def db_url(self, db_name: str) -> Union[URL, None]:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        if db_name == "lira_db":
            return URL.build(
                scheme="postgresql+asyncpg",
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_pass,
                path=f"/{self.db_base}",
            )
        elif db_name == "altitude_db":
            return URL.build(
                scheme="postgresql+asyncpg",
                host=self.altitude_db_host,
                port=self.altitude_db_port,
                user=self.altitude_db_user,
                password=self.altitude_db_pass,
                path=f"/{self.altitude_db_base}",
            )
        else:
            return

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
