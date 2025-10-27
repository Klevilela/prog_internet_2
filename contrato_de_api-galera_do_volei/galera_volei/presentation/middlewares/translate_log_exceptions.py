# translate_exception_middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from presentation.exceptions.HTTPException import AppException
from presentation.exceptions.HTTPNotFound import NotFoundException
from application.exceptions.domain_exceptions import DomainException

async def translate_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except DomainException as de:
        if isinstance(de, NotFoundException):
            return JSONResponse(status_code=404, content={"detail": str(de)})
        return JSONResponse(status_code=400, content={"detail": str(de)})
    except Exception as e:
        # Para qualquer outra exceção, deixa passar para o middleware global
        raise e
