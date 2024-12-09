from fastapi import Response
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

from spotify_clone.settings import  ALGO, JWT_SECRET


class AuthUtils():
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, pwd):
        return self.ph.hash(pwd)
    
    def verify_password(self, input_pwd, hash_pwd):
        try:
            return self.ph.verify(hash_pwd, input_pwd)
        except VerifyMismatchError:
            return False
    
    def jwt_encode(self, payload):
        return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)
    
    def create_token_payload(self, user: dict, token_type: str):
        payload = {
            "id": user["id"],
            "type": token_type,
            "iat": datetime.utcnow(),
        }
        
        if token_type == "access":
            payload.update({
                "name": user["username"],
                "email": user["email"],
                "exp": datetime.utcnow() + timedelta(minutes=15)
            })
        else:  # refresh token
            payload.update({
                "exp": datetime.utcnow() + timedelta(days=7)
            })
            
        return payload
    
    def get_access_token(self, user: dict):
        return self.jwt_encode(self.create_token_payload(user, "access"))
    
    def get_refresh_token(self, user: dict):
        return self.jwt_encode(self.create_token_payload(user, "refresh"))
    
    def set_cookies(self, key: str, value: str, max_age: int, response: Response):
        response.set_cookie(
                key=key,
                value=value,
                httponly=True,
                # secure=True,  
                samesite="lax",
                max_age=max_age,
            )
    