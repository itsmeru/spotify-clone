from fastapi import Response
import jwt

from spotify_clone.auth.auth_subject import AuthEvent, AuthSubject
from spotify_clone.settings import  ALGO, JWT_SECRET


class TokenService(AuthSubject):
    def __init__(self):
        super().__init__()

    async def refresh_token(self, refresh_token: str, response: Response):    
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[ALGO])
            if payload["type"] != "refresh":
                self.clear_auth_cookies(response)
                return self.create_response(AuthEvent.INVALID_TOKEN, response)
       
            user = self.db_users.get_user_by_id(payload["id"])
            if not user:
                return self.create_response(AuthEvent.INVALID_TOKEN, response)

            access_token = self.utils.get_access_token(user)
            refresh_token = self.utils.get_refresh_token(user)

            self.utils.set_cookie("access_token", access_token, 900, response)
            self.utils.set_cookie("refresh_token", refresh_token, 604800, response)
            
            return self.create_response(AuthEvent.TOKEN_REFRESH_SUCCESS, response)

        except jwt.ExpiredSignatureError:
            self.clear_auth_cookies(response)
            return self.create_response(AuthEvent.TOKEN_EXPIRED, response)
        except jwt.DecodeError:
            self.clear_auth_cookies(response)
            return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED, response)