from http import HTTPStatus
from fastapi import HTTPException


class AppExceptions(HTTPException):
    def __init__(self, status_code: HTTPException, detail: str):
        self.status_code: HTTPStatus = status_code
        self.detail: str = detail
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(AppExceptions):
    def __init__(self, status_code=HTTPStatus.NOT_FOUND, detail="Not found error."):
        super().__init__(status_code, detail)


class ConflictError(AppExceptions):
    def __init__(self, status_code=HTTPStatus.CONFLICT, detail="Conflic error."):
        super().__init__(status_code, detail)


class ExpiredTokenError(AppExceptions):
    def __init__(self, status_code=HTTPStatus.UNAUTHORIZED, detail="Token was expired."):
        super().__init__(status_code, detail)
