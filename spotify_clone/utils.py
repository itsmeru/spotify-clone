from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

from spotify_clone.settings import  ALGO, JWT_SECRET
from spotify_clone.auth.events import AuthEvent, AuthSubject, AuthError


class Utils(AuthSubject):
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
    
    def create_token_payload(self, user: dict, token_type: str) -> dict:
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