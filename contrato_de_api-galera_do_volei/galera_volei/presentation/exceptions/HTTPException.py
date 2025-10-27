from fastapi import HTTPException

class AppException(HTTPException):
    status_code:int

    def __init__(self, message:str, status_code:int = 400):
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=message)

