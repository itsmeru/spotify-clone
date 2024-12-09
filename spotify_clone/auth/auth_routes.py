import re
from typing import Optional
from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel, EmailStr, Field, validator

from spotify_clone.dependencies import get_token_service
from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices
from spotify_clone.services.token_services import TokenService

router = APIRouter(tags=["Auth"])

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SignOutRequest(BaseModel):
    user_id: str

class SignUpRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=128, description="Name cannot be empty")
    email: EmailStr = Field(..., max_length=128, description="Invalid email format")
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
    

@router.post("/signin", summary="User Sign In")
async def sign_in(request: SignInRequest, response: Response, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_in(request.dict(), response)

@router.post("/signup", summary="User Registration", )
async def sign_up(request: SignUpRequest, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_up(request.dict())

@router.delete("/signout", summary="User Sign Out")
async def sign_out(request: SignOutRequest, auth_service:  AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_out(request.user_id)

@router.put("/refresh-token", summary="Get Access Token")
async def refresh_token(response: Response, refresh_token:Optional[str] =  Cookie(None, alias="refreshToken"), token_service: TokenService = Depends(get_token_service)):
    return await token_service.get_token(response, refresh_token)


