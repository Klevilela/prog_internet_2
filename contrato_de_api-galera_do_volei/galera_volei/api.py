from fastapi import FastAPI, Request
from presentation.middlewares.global_error_middleware import global_error_middleware
from presentation.routes.index import router
from presentation.middlewares.log_middlewares import log_middleware
from presentation.middlewares.translate_log_exceptions import translate_exception_middleware

app = FastAPI()

app.middleware('http')(log_middleware)
app.middleware('http')(translate_exception_middleware)
app.middleware('http')(global_error_middleware)

app.include_router(router)