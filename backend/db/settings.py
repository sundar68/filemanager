import os
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, BaseModel, SecretStr, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


PROJECT_DIR = Path(__file__).resolve().parent.parent


env_file = str(PROJECT_DIR / ".env")



class DatabaseSettings(BaseModel):
    hostname: str = "localhost"
    username: str = "postgres"
    password: SecretStr
    port: int = 5432
    database: str = "typeface"


class CloudSettings(BaseModel):
    minio_access_key_id: str
    minio_secret_access_key: str
    minio_bucket_name: str
    minio_endpoint_url: str
    aws_region: str
    aws_access_key: str
    aws_secret_key: str
    aws_bucket_name: str
    cloud_provider: str


class Settings(BaseSettings):
    postgres: DatabaseSettings
    cloud: CloudSettings

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> URL:
        """
        Build the SQLAlchemy database URL using the asyncpg driver.
        This computed field ensures the URL is always up to date with your database settings.
        """
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres.username,
            password=self.postgres.password.get_secret_value(),
            host=self.postgres.hostname,
            port=self.postgres.port,
            database=self.postgres.database,
        )

    model_config = SettingsConfigDict(
        env_file=env_file,
        case_sensitive=False,
        env_nested_delimiter="__",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Loads the settings from the .env file using Pydantic.
    The lru_cache decorator ensures that settings are loaded only once.
    """
    print("Loading configuration from .env file")
    return Settings()
