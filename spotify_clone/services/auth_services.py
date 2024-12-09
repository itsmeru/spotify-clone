import json
from fastapi import Response

from spotify_clone.auth.auth_subject import AuthSubject, AuthEvent

class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        
    async def sign_up(self, user_data: dict):
        existing_user = self.db_utils.get_user_by_email(user_data["email"])
        if existing_user:
            return self.create_response(AuthEvent.EMAIL_EXISTS)
        hashed_password = self.auth_utils.hash_password(user_data["password"])

        user = self.db_utils.insert_data_to_users(user_data["email"], user_data["username"], hashed_password)
        if user:
            return self.create_response(event = AuthEvent.SIGN_UP_SUCCESS)
        
        return self.create_response(AuthEvent.CREATE_FAILED)

    async def sign_in(self, user_data: dict, response: Response):
        user = self.db_utils.get_user_by_email(user_data["email"])
        if not user:
            return self.create_response(AuthEvent.USER_NOT_FOUND)
                    
        if self.auth_utils.verify_password(user_data["password"], user["hashed_password"]):
            del user["hashed_password"]

            refresh_token = self.auth_utils.get_refresh_token(user)

            token_data = {
                "token": refresh_token,
            }
            
            self.redis_utils.set_verification_code(
                user['id'], 
                json.dumps(token_data),
            )
            self.auth_utils.set_cookie("refreshToken", refresh_token, 60400, response)
            
            return self.create_response(AuthEvent.SIGN_IN_SUCCESS, response)
        
        return self.create_response(AuthEvent.INVALID_PASSWORD)
    
    async def sign_out(self, user_id):
        self.redis_utils.delete_verification_code(user_id)
        return self.create_response(AuthEvent.SIGN_OUT_SUCCESS)

            
    
    
   

    


                


    

