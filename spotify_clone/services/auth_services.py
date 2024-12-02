from spotify_clone.auth.events import AuthSubject, AuthEvent
from spotify_clone.services.db import execute_query
from spotify_clone.utils import Utils
from spotify_clone.settings import ERROR_MESSAGES


class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        self.utils = Utils()
    
    async def sign_up(self, user_data: dict):
        existing_user = execute_query("SELECT id FROM users WHERE email = %s",(user_data["email"], ))
        if existing_user:
            return self.utils.create_error_response(400, ERROR_MESSAGES["EMAIL_EXISTS"], AuthEvent.SIGN_UP_FAILED)

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
        
        return self.utils.create_error_response(500, ERROR_MESSAGES["CREATE_FAILED"], AuthEvent.SIGN_UP_FAILED)

    async def sign_in(self,user_data: dict):
        email = user_data["email"]
        input_pwd = user_data["password"]

        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,))

        if not result:
            return self.utils.create_error_response(404, ERROR_MESSAGES["USER_NOT_FOUND"], AuthEvent.SIGN_IN_FAILED)
        
        
        user = result[0]
        hashed_pwd = user["hashed_password"]

        if self.utils.verify_password(input_pwd, hashed_pwd):
            del user["hashed_password"]
            self.notify(AuthEvent.SIGN_IN_SUCCESS, user) 
            return user
        
        return self.utils.create_error_response(400, ERROR_MESSAGES["INVALID_PASSWORD"], AuthEvent.SIGN_IN_FAILED)

    

