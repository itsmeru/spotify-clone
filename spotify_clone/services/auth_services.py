from fastapi import Response
from fastapi.responses import JSONResponse
import jwt
import httpx

from spotify_clone.auth.events import AuthSubject, AuthEvent
from spotify_clone.services.db_users import DBUsers
from spotify_clone.utils import Utils
from spotify_clone.settings import  ALGO, JWT_SECRET, GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI, GITHUB_CLIENT_SECRET


class AuthServices(AuthSubject):
    def __init__(self):
        super().__init__() 
        self.utils = Utils()
        self.db_users = DBUsers()
    
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
            return self.create_response(AuthEvent.USER_NOT_FOUND, response)
                    
        if self.utils.verify_password(user_data["password"], user["hashed_password"]):
            del user["hashed_password"]
            self.utils.setting_access_token(user, response)
            self.utils.setting_refresh_token(user, response)

            data = {"id": user["id"], "email": user["email"]}
            return self.create_response(AuthEvent.SIGN_IN_SUCCESS, response, data)
        
        self.clear_auth_cookies(response)
        return self.create_response(AuthEvent.INVALID_PASSWORD, response)
            
    async def refresh_token(self, refresh_token: str, response: Response):    
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[ALGO])
            if payload["type"] != "refresh":
                self.clear_auth_cookies(response)
                return self.create_response(AuthEvent.INVALID_TOKEN, response)
       
            user = self.db_users.get_user_by_id(payload["id"])
            if not user:
                return self.create_response(AuthEvent.INVALID_TOKEN, response)

            self.utils.setting_access_token(user, response)
            
            return self.create_response(AuthEvent.TOKEN_REFRESH_SUCCESS, response)

        except jwt.ExpiredSignatureError:
            self.clear_auth_cookies(response)
            return self.create_response(AuthEvent.TOKEN_EXPIRED, response)
        except jwt.DecodeError:
            self.clear_auth_cookies(response)
            return self.create_response(AuthEvent.TOKEN_REFRESH_FAILED, response)

    
    def clear_auth_cookies(self, response: Response):
        for key in ["access_token","refresh_token" ]:
            response.delete_cookie(key=key)
    
    def create_response(self, event: AuthEvent, response: Response = None, data=None,):
        content = {"status_code": event.value.status_code, "status_msg": event.value.message}
        self.notify(event, data)
        if response:
            response.status_code = event.value.http_status_code
            return content
        
        return JSONResponse(
            status_code=event.value.http_status_code, 
            content=content
        )

    async def github_login(self):
        params = {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": GITHUB_REDIRECT_URI,
            "scope": "user:email",
        }
        auth_url = f"https://github.com/login/oauth/authorize?{'&'.join(f'{k}={v}' for k, v in params.items())}"
        return {"url": auth_url}
    
    async def github_callback(self, code: str, response: Response):
        # 1. using code to get access token
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                "https://github.com/login/oauth/access_token",
                data = {
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                headers={"Accept": "application/json"}
            )
            token_data = token_res.json()
            access_token = token_data['access_token']
            # 2. using access token to get user info
            user_res = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )

            github_user = user_res.json()
            
            # 3. get email
            email_res = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )
            emails = email_res.json()
            primary_email = ""
            for email in emails:
                if email['primary']:
                    primary_email = email['email']
            
            if not primary_email:
                return self.create_response(AuthEvent.GITHUB_AUTH_FAILED, response)
            
            # 4. create users
            user = self.db_users.get_user_by_provider_id('github', str(github_user['id']))
            if not user:
                user = self.db_users.insert_data_to_users(email=primary_email,
                    username=github_user['login'],
                    provider='github',
                    provider_id=str(github_user['id']))
                
            self.utils.setting_access_token(user, response)
            self.utils.setting_refresh_token(user, response)

            return self.create_response(AuthEvent.GITHUB_AUTH_SUCCESS, response)
            

            


                


    

