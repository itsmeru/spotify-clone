from fastapi import APIRouter, Depends
from pydantic import BaseModel

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter()

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
async def sign_in(request: SignInRequest, auth_service:  AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_in(request.dict())