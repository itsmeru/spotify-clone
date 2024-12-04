from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel, EmailStr

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter(tags=["Auth"])

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

@router.delete("/signout", summary="User Sign Out")

async def sign_out(request: SignInRequest, response: Response, auth_service:  AuthServices = Depends(get_auth_service)):
    # return await auth_service.sign_in(request.dict(), response)
    pass
