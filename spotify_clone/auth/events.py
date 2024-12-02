from abc import ABC, abstractmethod
from enum import Enum

class AuthEvent(Enum):
    SIGN_IN_SUCCESS = "sign_in_success"
    SIGN_IN_FAILED = "sign_in_failed"
    SIGN_UP_SUCCESS = "sign_up_success"
    SIGN_UP_FAILED = "sign_up_failed"
    TOKEN_REFRESH_FAILED = "token_refresh_failed"

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
    