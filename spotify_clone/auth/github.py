from fastapi import APIRouter, Depends, Response

from spotify_clone.services.oauth_services import OAuthServices
from spotify_clone.dependencies import get_oauth_service

router = APIRouter(tags=["OAuth"])

@router.get("/github/login", summary="Github login")
async def github_login(oauth_service: OAuthServices = Depends(get_oauth_service)):
    return await oauth_service.github_login()

@router.get("/github/callback", summary="Github callback")
async def github_callback(response: Response, code: str, oauth_service: OAuthServices = Depends(get_oauth_service)):
    return await oauth_service.github_callback(code, response)
