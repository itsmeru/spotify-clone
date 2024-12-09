from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

from spotify_clone.dependencies import get_password_service
from spotify_clone.services.password_services import PasswordeSrvices

router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyPasswordRequest(BaseModel):
    email: EmailStr
    verify_code: str

@router.post("/forgot-password", summary="Request Password Reset")
async def forgot_password(emails: ForgotPasswordRequest, password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.forgot_password(emails.email)

@router.post("/verify-password", summary="Verify Reset Code")
async def forgot_password(verify_request: VerifyPasswordRequest, password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.verify_password(verify_request.verify_code, verify_request.email)
