from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from main.api.routes.router import api_router
from main.services import session

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def create_table():
    await session.create_table()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Get first error from validation errors list
    error_message = exc.errors()[0].get("msg")
    error_message = ""

    """
    Get list of error in form of multiple lines,
    each line represents an error that violates
    the constraints.
    """
    for error in exc.errors():
        error_message += error.get("msg")
        if exc.errors().index(error) != len(exc.errors()) - 1:  # Not last element
            error_message += "\n"

    return JSONResponse(
        content={"error_message": error_message},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        content={"error_message": exc.detail},
        status_code=exc.status_code,
    )
