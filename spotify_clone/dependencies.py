from spotify_clone.services.auth_services import AuthServices
from spotify_clone.services.oauth_services import OAuthServices
from spotify_clone.services.token_services import TokenService

def get_service_instance(service_class):
    def get_instance():
        if not hasattr(get_instance, '_instance'):
            get_instance._instance = service_class()
        return  get_instance._instance
    return get_instance

get_auth_service = get_service_instance(AuthServices)
get_oauth_service = get_service_instance(OAuthServices)
get_token_service = get_service_instance(TokenService)



