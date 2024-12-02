from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

ERROR_MESSAGES = {
    "EMAIL_EXISTS": "Email already registered",
    "USER_NOT_FOUND": "User not found",
    "INVALID_PASSWORD": "Invalid password",
    "CREATE_FAILED": "Failed to create user"
}
