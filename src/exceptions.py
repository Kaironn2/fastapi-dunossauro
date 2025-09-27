from typing import Literal

from fastapi import status
from fastapi.exceptions import HTTPException

allowed_status_codes = {
    'BAD_REQUEST': status.HTTP_400_BAD_REQUEST,
    'UNAUTHORIZED': status.HTTP_401_UNAUTHORIZED,
    'NOT_FOUND': status.HTTP_404_NOT_FOUND,
}

AllowedStatusCodes = Literal['BAD_REQUEST', 'UNAUTHORIZED', 'NOT_FOUND']


class AppError:
    @staticmethod
    def http_exception(status_code: AllowedStatusCodes, message: str) -> None:
        code = allowed_status_codes[status_code]
        raise HTTPException(detail=message, status_code=code)
