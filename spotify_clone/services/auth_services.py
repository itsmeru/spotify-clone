from fastapi import Response
from fastapi.responses import JSONResponse
import jwt

from spotify_clone.auth.events import AuthSubject, AuthError, AuthEvent
from spotify_clone.services.db import execute_query
from spotify_clone.utils import Utils
from spotify_clone.settings import  ALGO, JWT_SECRET


class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        self.utils = Utils()
    
    async def sign_up(self, user_data: dict):
        existing_user = execute_query("SELECT id FROM users WHERE email = %s",(user_data["email"], ))
        if existing_user:
            return self.create_error_response(AuthError.EMAIL_EXISTS, AuthEvent.SIGN_UP_FAILED)
        hashed_password = self.utils.hash_password(user_data["password"])

        user = self.insert_data_to_users(user_data["email"], user_data["username"], hashed_password)
        if user:
            self.notify(AuthEvent.SIGN_UP_SUCCESS, user) 
            return user
        
        return self.create_error_response(AuthError.CREATE_FAILED, AuthEvent.SIGN_UP_FAILED)

    async def sign_in(self, user_data: dict, response: Response):
        user = self.get_user_by_email(user_data["email"])
        if not user:
            return self.create_error_response(AuthError.USER_NOT_FOUND, AuthEvent.SIGN_IN_FAILED)
                    
        if self.utils.verify_password(user_data["password"], user["hashed_password"]):
            del user["hashed_password"]
            self.notify(AuthEvent.SIGN_IN_SUCCESS, user)

            access_token = self.utils.jwt_encode(self.utils.create_token_payload(user, "access"))
            refresh_token = self.utils.jwt_encode(self.utils.create_token_payload(user, "refresh"))

            self.cookie_setting("access_token", access_token, 900, response)
            self.cookie_setting("refresh_token", refresh_token, 604800, response)

            return {"status_code": "0000", "status_msg": "Success",}
        
        return self.create_error_response(AuthError.INVALID_PASSWORD, AuthEvent.SIGN_IN_FAILED)
            
    async def refresh_token(self, refresh_token: str, response: Response):    
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[ALGO])
            if payload["type"] != "refresh":
                return self.create_error_response(AuthError.INVALID_TOKEN, AuthEvent.TOKEN_REFRESH_FAILED)
       
            user = self.get_user_by_id(payload["id"])
            if not user:
                return self.create_error_response(AuthError.INVALID_TOKEN, AuthEvent.TOKEN_REFRESH_FAILED)

            new_access_token = self.utils.jwt_encode(self.utils.create_token_payload(user, "access"))

            self.cookie_setting("access_token", new_access_token, 900, response)
            
            return {"status_code": "0000", "status_msg": "Token refreshed successfully"}

        except jwt.ExpiredSignatureError:
            return self.create_error_response(AuthError.TOKEN_EXPIRED, AuthEvent.TOKEN_REFRESH_FAILED)
    
    def cookie_setting(self, key: str, value: str, max_age: int, response: Response):
        return response.set_cookie(
                key=key,
                value=value,
                httponly=True,
                # secure=True,  
                samesite="lax",
                max_age=max_age  
            )
    
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,))
        return result[0] if result else None
    
    def get_user_by_id(self, user_id):
        query = "SELECT id, username, email FROM users WHERE id = %s"
        result = execute_query(query, (user_id,))
        return result[0] if result else None
    
    def insert_data_to_users(self, email, username, hashed_password):
        query = """
        INSERT INTO users (email, username, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id, email, username, created_at
        """
        result = execute_query(query, (email, username, hashed_password))
        return result[0] if result else None
    
    def create_error_response(self, error: AuthError, event: AuthEvent):
        content = {"error_code": error.value.error_code, "status_msg": error.value.message}
        self.notify(event, content)
        return JSONResponse(status_code=error.value.status_code, content=content)

    

