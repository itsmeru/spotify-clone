import re
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, validator

from spotify_clone.dependencies import get_password_service
from spotify_clone.services.password_services import PasswordeSrvices

router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyPasswordRequest(BaseModel):
    email: EmailStr
    verify_code: str

class ChangePasswordRequest(BaseModel):
    password: str = Field(..., min_length=8, max_length=128)
    @validator('password')
    def password＿required_chars(cls, v):
       if not re.search(r'[A-Z]', v): 
           raise ValueError('Password must contain at least one uppercase letter')
       if not re.search(r'[a-z]', v): 
           raise ValueError('Password must contain at least one lowercase letter')
       if not re.search(r'\d', v):  
           raise ValueError('Password must contain at least one number')
       if not re.search(r'[@$!%*#?&]', v):  
           raise ValueError('Password must contain at least one special character')
       return v

@router.post("/forgot-password", summary="Request Password Reset")
async def forgot_password(emails: ForgotPasswordRequest, password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.forgot_password(emails.email)

@router.post("/verify-code", summary="Verify Reset Code")
async def  verify_code(verify_request: VerifyPasswordRequest, password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.verify_password(verify_request.verify_code, verify_request.email)

@router.post("/change-password", summary="Change Password")
async def change_password(password_request: ChangePasswordRequest, token: str = Depends(oauth2_scheme), password_service: PasswordeSrvices = Depends(get_password_service)):
    return password_service.change_password(token, password_request.password)