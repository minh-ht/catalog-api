from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from main.api.routes.router import api_router
from main.services.database.init_db import init_db

init_db()
app = FastAPI()

app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_message = ""

    for idx in range(len(exc.errors())):
        error_message += exc.errors()[idx].get("msg")
        if idx < len(exc.errors()) - 1:
            error_message += "\n"

    return JSONResponse(content={"error_message": error_message},
                        status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"error_message": exc.detail},
                        status_code=exc.status_code)
