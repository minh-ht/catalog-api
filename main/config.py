import os

from pydantic import BaseSettings

environment = os.getenv("ENVIRONMENT", "local")


class Settings(BaseSettings):
    # Database config
    SQL_ALCHEMY_DATABASE_URL: str

    # Security config
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRED_MINUTES: int

    class Config:
        env_file = f"{environment}.env"


settings = Settings()
