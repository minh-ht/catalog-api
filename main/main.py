from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from main.api.routes.router import api_router
from main.services.database.session import create_table

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def clear_table():
    await create_table()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_message = ""

    for index in range(len(exc.errors())):
        error_message += exc.errors()[index].get("msg")
        if index < len(exc.errors()) - 1:
            error_message += "\n"

    return JSONResponse(content={"error_message": error_message}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"error_message": exc.detail}, status_code=exc.status_code)
