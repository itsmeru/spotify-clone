from abc import ABC, abstractmethod

from .auth_events import AuthEvent

class Observer(ABC):
    @abstractmethod
    def update(self, event:AuthEvent, data: dict):
        pass

class LoggingObserver(Observer):
    def update(self, event: AuthEvent, data: dict):
        print(f"Auth event: {event.value}, Data: {data}")
