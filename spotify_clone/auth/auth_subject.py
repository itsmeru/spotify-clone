from fastapi import Response
from fastapi.responses import JSONResponse

from .auth_events import AuthEvent
from .auth_observers import LoggingObserver, Observer
from spotify_clone.auth_utils import AuthUtils
from spotify_clone.db_utils import  DBUtils
from spotify_clone.redis_utils import RedisUtils

class AuthSubject:
    def __init__(self):
        self.db_utils =  DBUtils()
        self.auth_utils = AuthUtils()
        self.redis_utils = RedisUtils()
        self._observers = []
        self.attach(LoggingObserver())

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, event: AuthEvent, data: dict):
        for observer in self._observers:
            observer.update(event, data)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def create_response(self, event: AuthEvent, response: Response = None, data=None,):
            content = {
                "status_code": event.value.status_code,
                "status_msg": event.value.message,
                "data": data if data is not None else []
            }
            self.notify(event, data)
            if response:
                response.status_code = event.value.http_status_code
                return content
            
            return JSONResponse(
                status_code=event.value.http_status_code, 
                content=content
            )
    
    