from passlib.context import CryptContext

from spotify_clone.auth.events import AuthSubject
from spotify_clone.services.db import execute_query

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthServices(AuthSubject):
    def __init__(self):
        self.pwd_context = pwd_context

    async def sign_up(self, user_data: dict):
        existing_user = execute_query("SELECT id FROM users WHERE email = %s",(user_data["email"], ))
        if existing_user:
            return  {"error": "Email already registered"}

        email = user_data["email"]
        username = user_data["username"]
        hashed_password = self.hash_password(user_data["password"])

        query = """
        INSERT INTO users (email, username, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id, email, username, created_at
        """
    
        result = execute_query(query, (email, username, hashed_password))
        return result[0] if result else None

    async def sign_in(self,user_data: dict):
        email = user_data["email"]
        input_pwd = user_data["password"]

        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,))

        if not result:
            return {"error": "User not found"}
        
        user = result[0]
        hashed_pwd = user["hashed_password"]

        if self.verify_password(input_pwd, hashed_pwd):
            del user["hashed_password"]
            return user
        
        return {"error": "Invalid password"}

    def hash_password(self, pwd):
        return self.pwd_context.hash(pwd)
    
    def verify_password(self, input_pwd, hash_pwd):
        return self.pwd_context.verify(input_pwd, hash_pwd)

