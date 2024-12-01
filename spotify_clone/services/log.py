import logging
from auth.events import Observer, AuthEvent

def setup_logger():
    logger = logging.getLogger(__name__) 

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

    file_handler = logging.FileHandler('logging.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class LoggingObserver(Observer):
    def __init__(self):
        self.logger = setup_logger()
        
    def update(self, event: AuthEvent, data: dict):
        if event == AuthEvent.SIGN_IN_SUCCESS:
            self.logger.info(f"User login successful: {data['email']}")
        elif event == AuthEvent.SIGN_IN_FAILED:
            self.logger.warning(f"Login failed for user: {data['email']}")
        elif event == AuthEvent.SIGN_UP_SUCCESS:
            self.logger.info(f"New user registered: {data['email']}")
        elif event == AuthEvent.SIGN_UP_FAILED:
            self.logger.error(f"Registration failed: {data['email']}, reason: {data.get('error', 'unknown')}")

