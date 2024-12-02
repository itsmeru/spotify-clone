from fastapi.responses import JSONResponse

from spotify_clone.auth.events import AuthEvent
from spotify_clone.settings import PWD_CONTEXT

class Utils:
    def __init__(self):
        self.pwd_context = PWD_CONTEXT

    def hash_password(self, pwd):
        return self.pwd_context.hash(pwd)
    
    def verify_password(self, input_pwd, hash_pwd):
        return self.pwd_context.verify(input_pwd, hash_pwd)
    
    def create_error_response(self,  status_code: int, content: str, event: AuthEvent):
        content = {"error": content}
        self.notify(event, content)
        return JSONResponse(status_code=status_code, content=content)
