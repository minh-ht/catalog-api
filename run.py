from fastapi import FastAPI

from main.api.api import api_router
from main.services.database.init_db import init_db

init_db()
app = FastAPI()

app.include_router(api_router)