from fastapi import APIRouter
from pydantic import BaseModel

from spotify_clone.services.auth_services import AuthServices

router = APIRouter()
auth_service = AuthServices()

class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signup")
async def sign_up(request: SignUpRequest):
    return await auth_service.sign_up(request.dict())