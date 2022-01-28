from main.services.database.session import engine
from main import models


def init_db():
    models.base_class.Base.metadata.create_all(bind=engine)
