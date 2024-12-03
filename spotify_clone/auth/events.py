from abc import ABC, abstractmethod
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
    TOKEN_REFRESH_FAILED = StatusInfo(400, "9999", "Token refresh failed")
    SIGN_IN_SUCCESS = StatusInfo(200, "0000", "Sign in success")
    SIGN_UP_SUCCESS = StatusInfo(200, "0000", "Sign up success")
    TOKEN_REFRESH_SUCCESS = StatusInfo(200, "0000", "Token_refresh_success")
    GITHUB_AUTH_FAILED = StatusInfo(401, "9999", "Github auth failed")
    GITHUB_AUTH_SUCCESS = StatusInfo(200, "0000", "Github auth success")


class Observer(ABC):
    @abstractmethod
    def update(self, event:AuthEvent, data: dict):
        pass

class LoggingObserver(Observer):
    def update(self, event: AuthEvent, data: dict):
        print(f"Auth event: {event.value}, Data: {data}")

class AuthSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, event: AuthEvent, data: dict):
        for observer in self._observers:
            observer.update(event, data)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
    