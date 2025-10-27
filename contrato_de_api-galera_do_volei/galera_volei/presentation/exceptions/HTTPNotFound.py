from .HTTPException import AppException

class NotFoundException(AppException):
    def __init__(self, message:str):
        super().__init__(message, 404)
