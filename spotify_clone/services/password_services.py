import datetime
import email.message
import random

from spotify_clone.auth.auth_subject import AuthSubject, AuthEvent
from spotify_clone.redis_utils import RedisUtils

class PasswordeSrvices(AuthSubject):
    def __init__(self):
        super().__init__()
        self.redis_utils = RedisUtils()
    
    async def forgot_password(self, email: str):
        user = self.db_users.get_user_by_email(email)
        if not user:
            return self.create_response(AuthEvent.USER_NOT_FOUND)
        
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = datetime.utcnow() + datetime.timedelta(minutes=5)

        self.redis_utils.set_verification_code(email, verification_code, expires_at)