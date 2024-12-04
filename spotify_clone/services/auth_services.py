from fastapi import Response

from spotify_clone.auth.auth_subject import AuthSubject, AuthEvent

class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        
    async def sign_up(self, user_data: dict):
        existing_user = self.db_users.get_user_by_email(user_data["email"])
        if existing_user:
            return self.create_response(AuthEvent.EMAIL_EXISTS)
        hashed_password = self.utils.hash_password(user_data["password"])

        user = self.db_users.insert_data_to_users(user_data["email"], user_data["username"], hashed_password)
        if user:
            data = {"id": user["id"], "email": user["email"]}
            return self.create_response(event = AuthEvent.SIGN_UP_SUCCESS, data = data)
        
        return self.create_response(AuthEvent.CREATE_FAILED)

    async def sign_in(self, user_data: dict, response: Response):
        user = self.db_users.get_user_by_email(user_data["email"])
        if not user:
            self.clear_auth_cookies(response)
            return self.create_response(AuthEvent.USER_NOT_FOUND)
                    
        if self.utils.verify_password(user_data["password"], user["hashed_password"]):
            del user["hashed_password"]

            access_token = self.utils.get_access_token(user)
            refresh_token = self.utils.get_refresh_token(user)

            self.utils.set_cookie("access_token", access_token, 900, response)
            self.utils.set_cookie("refresh_token", refresh_token, 604800, response)

            data = {"id": user["id"], "email": user["email"]}
            return self.create_response(AuthEvent.SIGN_IN_SUCCESS, response, data)
        
        self.clear_auth_cookies(response)
        return self.create_response(AuthEvent.INVALID_PASSWORD)
    
    async def sign_out(self, response: Response):
        self.clear_auth_cookies(response)
        return self.create_response(AuthEvent.SIGN_OUT_SUCCESS)

            
    
    
   

    


                


    

