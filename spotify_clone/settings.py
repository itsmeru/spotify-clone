from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("ALGORITHM")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = "http://127.0.0.1:8000/api/v1/auth/github/callback"
GITHUB_OAUTH_URL = "https://github.com/login/oauth/authorize"
