from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from spotify_clone.auth import sign_in, sign_up, sign_out, github, refresh_token, forgot_password
from spotify_clone.services.db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0].get("msg")
    return JSONResponse(
        status_code=422,
        content={
            "status_code": "1003",  
            "status_msg": error_msg,
            "data": []
        }
    )

app.include_router(sign_up.router, prefix="/api/v1")
app.include_router(sign_in.router, prefix="/api/v1/auth")
app.include_router(sign_out.router, prefix="/api/v1/auth")
app.include_router(github.router, prefix="/api/v1/auth")
app.include_router(refresh_token.router, prefix="/api/v1/auth")
app.include_router(forgot_password.router, prefix="/api/v1/auth")


