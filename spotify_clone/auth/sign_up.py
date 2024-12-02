from fastapi import APIRouter, Depends
from pydantic import BaseModel

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter()

class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signup")

async def sign_up(request: SignUpRequest, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_up(request.dict())