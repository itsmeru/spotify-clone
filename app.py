from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from spotify_clone.auth import auth_routes, github, forgot_password
from spotify_clone.services.db import init_db, close_pool

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.on_event("shutdown")
async def shutdown_event():
    close_pool()

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

app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(github.router, prefix="/api/v1/auth")
app.include_router(forgot_password.router, prefix="/api/v1/auth")


