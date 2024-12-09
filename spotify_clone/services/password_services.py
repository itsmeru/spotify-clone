import smtplib
import random
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

from spotify_clone.auth.auth_subject import AuthSubject, AuthEvent
from spotify_clone.redis_utils import RedisUtils

class PasswordeSrvices(AuthSubject):
    def __init__(self):
        super().__init__()
        self.redis_utils = RedisUtils()
    
    def forgot_password(self, emails: str):
        user = self.db_utils.get_user_by_email(emails)
        if not user:
            return self.create_response(AuthEvent.USER_NOT_FOUND)
        
        try:
            verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            expires_in_seconds = 300

            msg = MIMEText(
                    f"您的驗證碼是：{verification_code}\n"
                    f"此驗證碼將在 5 分鐘後過期。"
                )
            msg["From"] = "cat821016@gmail.com"
            msg["To"] =  emails
            msg["Subject"] = "密碼重置驗證碼"
            
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("cat821016@gmail.com", os.getenv("EMAIL_PWD"))
            server.send_message(msg)
            server.close()

    
            self.redis_utils.set_verification_code(emails, verification_code, expires_in_seconds)

            return self.create_response(AuthEvent.EMAIL_SENT)
        
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
            return self.create_response(AuthEvent.EMAIL_SEND_FAILED)
    
    def verify_password(self, verify_code: str, email: str):
        stored_code = self.redis_utils.get_verification_code(email)
        if not stored_code:
            return self.create_response(AuthEvent.VERIFICATION_CODE_EXPIRED)
        
        if stored_code != verify_code:
            return self.create_response(AuthEvent.INVALID_VERIFICATION_CODE)

        self.redis_utils.delete_verification_code(email)

        return self.create_response(AuthEvent.VERIFICATION_CODE_SUCCESS)