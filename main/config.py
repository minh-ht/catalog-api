from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Catalog"
    items_per_page: int = 20

    # Database config
    SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://" \
                               "minhhoang:lighT023@localhost/catalog"

    # Security config
    SECRET_KEY = "4ca3722e7e3649a19fdea8c1ac2db5" \
                 "ebb7bb59b8d5c49a664329239d42f6acea"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
