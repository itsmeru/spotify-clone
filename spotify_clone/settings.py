from dotenv import load_dotenv
import os

load_dotenv

ERROR_MESSAGES = {
    "EMAIL_EXISTS": "Email already registered",
    "USER_NOT_FOUND": "User not found",
    "INVALID_PASSWORD": "Invalid password",
    "CREATE_FAILED": "Failed to create user",
    "INVALID_TOKEN": "Invalid token type"
}
JWT_SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("ALGORITHM")
