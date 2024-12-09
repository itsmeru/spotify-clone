import json
from fastapi import Response
import jwt

from spotify_clone.auth.auth_subject import AuthEvent, AuthSubject
from spotify_clone.settings import  ALGO, JWT_SECRET


class TokenService(AuthSubject):
    def __init__(self):
        super().__init__()

    async def get_token(self, response:Response, refresh_token: str):   
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[ALGO])
            user_id = payload.get("id")

            stored_data = self.redis_utils.get_verification_code(user_id)
            if not stored_data:
                return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED)
            
            stored_token = json.loads(stored_data).get("token")
        
            if stored_token != refresh_token:
                return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED)
            
            user_data = self.db_utils.get_user_by_id(user_id)
            if not user_data:
                return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED)
            
            access_token = self.auth_utils.get_access_token(user_data)
            new_refresh_token = self.auth_utils.get_refresh_token(user_data)

            token_data = {
                "token": new_refresh_token,
            }
            self.redis_utils.set_verification_code(
                user_id, 
                json.dumps(token_data),
            )

            self.auth_utils.set_cookies("refreshToken", new_refresh_token, 60400, response)
            
            return self.create_response(AuthEvent.TOKEN_REFRESH_SUCCESS,data = {"access_token": access_token} )

        except jwt.ExpiredSignatureError:
            return self.create_response(AuthEvent.TOKEN_EXPIRED)
        except jwt.DecodeError :
            return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED)