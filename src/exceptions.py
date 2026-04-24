from http import HTTPStatus
from fastapi import HTTPException


class AppExceptions(HTTPException):
    def __init__(self, status_code: HTTPException, detail: str):
        self.status_code: HTTPStatus = status_code
        self.detail: str = detail
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(AppExceptions):
    def __init__(self, status_code=HTTPStatus.NOT_FOUND, detail="Not Found."):
        super().__init__(status_code, detail)