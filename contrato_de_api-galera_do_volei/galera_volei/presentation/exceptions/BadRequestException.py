from .HTTPException import AppException
...

class BadRequestException(AppException):
    def __init__(self, message, status_code = 400):
        super().__init__(message, status_code)