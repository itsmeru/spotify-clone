from datetime import datetime, timedelta
from fastapi import Response

import jwt

from spotify_clone.auth.events import AuthSubject, AuthEvent
from spotify_clone.services.db import execute_query
from spotify_clone.utils import Utils
from spotify_clone.settings import ERROR_MESSAGES, ALGO, JWT_SECRET


class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        self.utils = Utils()
    
    async def sign_up(self, user_data: dict):
        existing_user = execute_query("SELECT id FROM users WHERE email = %s",(user_data["email"], ))
        if existing_user:
            return self.utils.create_error_response(400, 1002, ERROR_MESSAGES["EMAIL_EXISTS"], AuthEvent.SIGN_UP_FAILED)

        email = user_data["email"]
        username = user_data["username"]
        hashed_password = self.utils.hash_password(user_data["password"])

        query = """
        INSERT INTO users (email, username, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id, email, username, created_at
        """
    
        result = execute_query(query, (email, username, hashed_password))
        if result:
            user_info = result[0]
            self.notify(AuthEvent.SIGN_UP_SUCCESS, user_info) 
            return user_info
        
        return self.utils.create_error_response(500, 9999, ERROR_MESSAGES["CREATE_FAILED"], AuthEvent.SIGN_UP_FAILED)

    async def sign_in(self, user_data: dict, response: Response):
        email = user_data["email"]
        input_pwd = user_data["password"]

        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,))

        if not result:
            return self.utils.create_error_response(404, 9999, ERROR_MESSAGES["USER_NOT_FOUND"], AuthEvent.SIGN_IN_FAILED)
        
        
        user = result[0]
        hashed_pwd = user["hashed_password"]

        if self.utils.verify_password(input_pwd, hashed_pwd):
            del user["hashed_password"]
            self.notify(AuthEvent.SIGN_IN_SUCCESS, user)

            access_token_payload = {
                "id": user["id"],
                "name": user["username"],
                "email": user["email"],
                "type": "access",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }
            
            refresh_token_payload = {
                "id": user["id"],
                "type": "refresh",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(days=7)
            }

            access_token = jwt.encode(
                access_token_payload, 
                JWT_SECRET, 
                algorithm=ALGO
            )
            refresh_token = jwt.encode(
                refresh_token_payload, 
                JWT_SECRET, 
                algorithm=ALGO
            )

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                # secure=True,  
                samesite="lax",  
                max_age=900  
            )
            
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                # secure=True,
                samesite="lax",
                max_age=604800  
            )
            
            return {
                "status_code": "0000",
                "status_msg": "Success",
            }
        
        return self.utils.create_error_response(400, 9999, ERROR_MESSAGES["INVALID_PASSWORD"], AuthEvent.SIGN_IN_FAILED)
    
    async def refresh_token(self, refresh_token: str, response: Response):    
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[ALGO])
            if payload["type"] != "refresh":
                return self.utils.create_error_response(401, 9999, ERROR_MESSAGES["INVALID_TOKEN"], AuthEvent.TOKEN_REFRESH_FAILED)
            
            user_id = payload["id"]
            query = "SELECT id, username, email FROM users WHERE id = %s"
            result = execute_query(query, (user_id,))

            if not result:
                return self.utils.create_error_response(401, 9999, ERROR_MESSAGES["INVALID_TOKEN"], AuthEvent.TOKEN_REFRESH_FAILED)

            user = result[0]

            new_access_token_payload = {
                "id": user["id"],
                "name": user["username"],
                "email": user["email"],
                "type": "access",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }

            new_access_token = jwt.encode(
                new_access_token_payload,
                JWT_SECRET,
                algorithm=ALGO
            )

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                # secure=True,  
                samesite="lax",
                max_age=900  
            )

            return {
                "status_code": "0000",
                "status_msg": "Token refreshed successfully"
            }

        except jwt.ExpiredSignatureError:
            return self.utils.create_error_response(
                401, 
                9999, 
                "Refresh token expired", 
                AuthEvent.TOKEN_REFRESH_FAILED
            )
    

