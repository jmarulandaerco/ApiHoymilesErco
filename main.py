from App.authentication.token import AuthService
from App.enrg.send_data import PostRequester
from App.reports import HoymileReport
from utils.configHandler import ConfigHandler, ConfigHandlerKey
from utils.logger import LoggerHandler
from datetime import datetime, time
import pytz

if __name__ == "__main__":
    # start = time.time()

    config_handler = ConfigHandler("config.ini")
    config_key = ConfigHandlerKey("key.ini")
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    key = config_key.get_key()
    colombia_tz = pytz.timezone("America/Bogota")
    now = datetime.now(colombia_tz).replace(minute=0, second=0, microsecond=0)
    hour = now.hour
    hoymiles = HoymileReport(logger=logger, config_data=config_handler, key=key, hour=int(hour))
    data_plants=hoymiles.order_information_plants()
    
    payloads=hoymiles.create_payload(data_plants)
    hoymiles.information_processing(data_plants)
    
    get_token= AuthService(logger=logger,url=config_handler.get_url_token(),credential=config_key.get_credentials())
    token=get_token.get_token()
    send_data = PostRequester(url=config_handler.get_url_enrg(),token=token,logger= logger,payloads=payloads)
    send_data.send_post_requests()
    # end = time.time()
    # duration = end - start
    # print(f"Tiempo de ejecución: {duration:.2f} segundos")


    