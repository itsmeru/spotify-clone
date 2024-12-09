from enum import Enum
from typing import NamedTuple

class StatusInfo(NamedTuple):
    http_status_code: int
    status_code: str
    message: str

class AuthEvent(Enum):
    EMAIL_EXISTS = StatusInfo(400, "1002", "Email already exists")
    USER_NOT_FOUND = StatusInfo(404, "9999", "User not found")
    INVALID_PASSWORD = StatusInfo(400, "9999", "Invalid password")
    CREATE_FAILED = StatusInfo(500, "9999", "Failed to create user")
    TOKEN_EXPIRED = StatusInfo(401, "9999", "Token has expired")
    INVALID_TOKEN = StatusInfo(401, "9999", "Invalid token")
    TOKEN_REFRESH_FAILED = StatusInfo(401, "9999", "Token refresh failed")
    SIGN_IN_SUCCESS = StatusInfo(200, "0000", "Sign in success")
    SIGN_UP_SUCCESS = StatusInfo(200, "0000", "Sign up success")
    SIGN_OUT_SUCCESS = StatusInfo(200, "0000", "Sign out success")
    TOKEN_REFRESH_SUCCESS = StatusInfo(200, "0000", "Token_refresh_success")
    GITHUB_AUTH_FAILED = StatusInfo(401, "9999", "Github auth failed")
    GITHUB_AUTH_SUCCESS = StatusInfo(200, "0000", "Github auth success")
    EMAIL_SENT = StatusInfo(200, "0000", "email sent success")
    EMAIL_SEND_FAILED = StatusInfo(400, "9999", "email send failed")
    VERIFICATION_CODE_EXPIRED =  StatusInfo(401, "9999", "verification code has expired")
    INVALID_VERIFICATION_CODE = StatusInfo(400, "9999", "invalid verification code")
    VERIFICATION_CODE_SUCCESS = StatusInfo(200, "0000", "verify success")
    UPDATE_PASSWORD_FAILED = StatusInfo(400, "9999", "update password failed")
    UPDATE_PASSWORD_SUCCESS =  StatusInfo(200, "0000", "update password success")



