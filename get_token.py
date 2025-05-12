from App.authentication.token import AuthService
from utils.configHandler import ConfigHandler, ConfigHandlerKey
from utils.logger import LoggerHandler

config_handler = ConfigHandler("config.ini")
config_key = ConfigHandlerKey("key.ini")
url_token = config_handler.get_url_token()
credential_token = config_key.get_credential_token()

logger_handler = LoggerHandler()
logger = logger_handler.get_logger()

auth_service = AuthService(logger=logger, url=url_token, credential= credential_token)
token = auth_service.get_token()
print(token)