import re
from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from spotify_clone.auth.events import AuthEvent, AuthSubject


class Utils(AuthSubject):
    def __init__(self):
        super().__init__() 
        self.ph = PasswordHasher()

    def hash_password(self, pwd):
        return self.ph.hash(pwd)
    
    def verify_password(self, input_pwd, hash_pwd):
        try:
            return self.ph.verify(hash_pwd, input_pwd)
        except VerifyMismatchError:
            return False
    
    def create_error_response(self,  status_code: int, error_code: int, content: str, event: AuthEvent):
        content = {"error_code": error_code, "status_msg": content}
        self.notify(event, content)
        return JSONResponse(status_code=status_code, content=content)
