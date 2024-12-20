import json
import httpx
from fastapi import Response

from spotify_clone.auth.auth_subject import AuthSubject, AuthEvent
from spotify_clone.services.auth_services import AuthServices
from spotify_clone.settings import  GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI, GITHUB_CLIENT_SECRET


class OAuthServices(AuthSubject):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthServices()
    
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
                return self.create_response(AuthEvent.GITHUB_AUTH_FAILED)
            
            # 4. create users
            oauth_user = self.db_utils.get_user_by_provider_id('github', str(github_user['id']))
            auth_user = self.db_utils.get_user_by_email(primary_email)

            if oauth_user:  
                user = oauth_user
            else:
                if auth_user:
                    return self.create_response(AuthEvent.EMAIL_EXISTS)

                user = self.db_utils.insert_data_to_users(email=primary_email,
                    username=github_user['login'],
                    provider='github',
                    provider_id=str(github_user['id']))
                
            refresh_token = self.auth_utils.get_refresh_token(user)
            access_token = self.auth_utils.get_access_token(user)
            
            token_data = {
                "token": refresh_token,
            }

            self.redis_utils.set_verification_code(
                user['id'], 
                json.dumps(token_data),
            )

            self.auth_utils.set_cookies("refreshToken", refresh_token, 60400, response)

            return self.create_response(AuthEvent.GITHUB_AUTH_SUCCESS, data = {"access_token": access_token, "user_id": user['id']})
            

            