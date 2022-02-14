from fastapi import status
from fastapi.exceptions import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, error_message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)


class UnauthorizedException(HTTPException):
    def __init__(self, error_message: str = "User needs to authenticate"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)


class ForbiddenException(HTTPException):
    def __init__(self, error_message: str = "User does not have permission"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)


class NotFoundException(HTTPException):
    def __init__(self, error_message: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
