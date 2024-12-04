from fastapi import APIRouter, Cookie, Depends, Response

from spotify_clone.dependencies import get_token_service
from spotify_clone.services.token_services import TokenService

router = APIRouter(tags=["Auth"])

@router.put("/refresh", summary="Refresh Access Token")
async def refresh_token(response: Response, refresh_token: str = Cookie(None), token_service: TokenService = Depends(get_token_service)):
    return await token_service.refresh_token(refresh_token, response)