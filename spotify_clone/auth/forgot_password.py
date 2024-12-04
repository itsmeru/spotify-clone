from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from spotify_clone.dependencies import get_password_service
from spotify_clone.services.password_services import PasswordeSrvices

router = APIRouter(tags=["Auth"])

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password", summary="Request Password Reset")
async def forgot_password(email: ForgotPasswordRequest, password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.forgot_password(email)
