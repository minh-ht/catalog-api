from pydantic import BaseSettings


class Settings(BaseSettings):
    ITEMS_PER_PAGE: int = 20

    # Database config
    SQL_ALCHEMY_DATABASE_URL = "mysql+aiomysql://minhhoang:lighT023@localhost/catalog"

    # Security config
    JWT_SECRET_KEY = "4ca3722e7e3649a19fdea8c1ac2db5ebb7bb59b8d5c49a664329239d42f6acea"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRED_MINUTES = 30


settings = Settings()
