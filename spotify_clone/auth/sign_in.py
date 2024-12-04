from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel, EmailStr

from spotify_clone.dependencies import get_auth_service, get_token_service
from spotify_clone.services.auth_services import AuthServices
from spotify_clone.services.token_services import TokenService

router = APIRouter(tags=["Auth"])

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signin", summary="User Sign In")

async def sign_in(request: SignInRequest, response: Response, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_in(request.dict(), response)

@router.put("/refresh", summary="Refresh Access Token")
async def refresh_token(response: Response, refresh_token: str = Cookie(None), token_service: TokenService = Depends(get_token_service)):
    return await token_service.refresh_token(refresh_token, response)