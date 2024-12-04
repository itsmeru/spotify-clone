from fastapi import APIRouter, Depends, Response

from spotify_clone.dependencies import get_auth_service
from spotify_clone.services.auth_services import AuthServices

router = APIRouter(tags=["Auth"])

@router.delete("/signout", summary="User Sign Out")
async def sign_out(response: Response, auth_service:  AuthServices = Depends(get_auth_service)):
    return await auth_service.sign_out(response)


