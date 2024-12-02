from spotify_clone.services.auth_services import AuthServices
from spotify_clone.auth.events import LoggingObserver

def get_auth_service():
    if hasattr(get_auth_service, '_instance'):
        return get_auth_service._instance
    
    auth_services = AuthServices()
    logging_observer = LoggingObserver()

    auth_services.attach(logging_observer)

    get_auth_service._instance = auth_services

    return auth_services