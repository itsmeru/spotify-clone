from fastapi import APIRouter
from pydantic import BaseModel

from spotify_clone.services.auth_services import AuthServices

router = APIRouter()
auth_service = AuthServices()

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
async def sign_in(request: SignInRequest):
    return await auth_service.sign_in(request.dict())