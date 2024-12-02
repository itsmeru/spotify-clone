from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple

class ErrorInfo(NamedTuple):
    status_code: int
    error_code: str
    message: str

class AuthEvent(Enum):
    SIGN_IN_SUCCESS = "sign_in_success"
    SIGN_IN_FAILED = "sign_in_failed"
    SIGN_UP_SUCCESS = "sign_up_success"
    SIGN_UP_FAILED = "sign_up_failed"
    TOKEN_REFRESH_FAILED = "token_refresh_failed"

class AuthError(Enum):
    EMAIL_EXISTS = ErrorInfo(400, "1002", "Email already exists")
    USER_NOT_FOUND = ErrorInfo(404, "9999", "User not found")
    INVALID_PASSWORD = ErrorInfo(400, "9999", "Invalid password")
    CREATE_FAILED = ErrorInfo(500, "9999", "Failed to create user")
    TOKEN_EXPIRED = ErrorInfo(401, "9999", "Token has expired")
    INVALID_TOKEN = ErrorInfo(401, "9999", "Invalid token")

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
    