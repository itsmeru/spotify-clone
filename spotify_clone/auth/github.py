from fastapi import APIRouter, Depends, Response

from spotify_clone.services.auth_services import AuthServices
from spotify_clone.dependencies import get_auth_service
router = APIRouter()

@router.get("/github/login")
async def github_login(auth_service: AuthServices = Depends(get_auth_service)):
    return await auth_service.github_login()

@router.get("/github/callback")
async def github_callback(code: str,  response: Response, auth_service: AuthServices = Depends(get_auth_service)):
    print(f"Received callback with code: {code}") 
    return await auth_service.github_callback(code, response)
