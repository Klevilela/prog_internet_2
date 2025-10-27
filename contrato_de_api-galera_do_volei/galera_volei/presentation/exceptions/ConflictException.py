from .HTTPException import AppException

class ConflictException(AppException):
    def __init__(self, message:str):
        super().__init__(message, 409)