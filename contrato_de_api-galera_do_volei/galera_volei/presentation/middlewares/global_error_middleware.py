from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from presentation.exceptions.HTTPException import AppException
from presentation.exceptions.HTTPNotFound import NotFoundException


app = FastAPI()

@app.middleware("http")
async def global_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except AppException as ae:
        # Trata suas exceções personalizadas
        return JSONResponse(
            status_code=ae.status_code,
            content={"detail": str(ae)}
        )
    except NotFoundException as ne:
        return JSONResponse(
            status_code=404,
            content={"detail": str(ne)}
        )
    except FastAPIHTTPException as fe:
        # Pega exceções do FastAPI nativas
        return JSONResponse(
            status_code=fe.status_code,
            content={"detail": fe.detail}
        )
    except Exception as e:
        # Qualquer outro erro não tratado
        return JSONResponse(
            status_code=500,
            content={"detail": f"{str(e)}"}
        )
