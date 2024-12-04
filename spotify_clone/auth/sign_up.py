from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr, validator
import re
from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter(tags=["User"])

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
    
@router.post("/users", summary="User Registration", )
async def sign_up(request: SignUpRequest, auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_up(request.dict())