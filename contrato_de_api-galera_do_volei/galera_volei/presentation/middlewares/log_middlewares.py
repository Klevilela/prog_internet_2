from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

async def log_middleware(request: Request, call_next):
    try:
        
        print(f"[LOG] {request.method} {request.url.path}")
        response = await call_next(request)
        print(f"[LOG] Status: {response.status_code}")

        return response

    except HTTPException as exc:
        
        print(f"[EXCEPTION] HTTPException: {exc.detail}")
        raise exc

    except Exception as e:
        
        print(f"[ERROR] Erro inesperado: {str(e)}")
        raise e
