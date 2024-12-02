from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter()

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
async def sign_in(request: SignInRequest, response: Response, auth_service:  AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_in(request.dict(), response)

@router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None), auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.refresh_token(refresh_token, response)