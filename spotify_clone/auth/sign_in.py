from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, EmailStr

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter(tags=["Auth"])

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signin", summary="User Sign In")
async def sign_in(request: SignInRequest, response: Response, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_in(request.dict(), response)

