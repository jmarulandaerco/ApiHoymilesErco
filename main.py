from App.reports import HoymileReport
from utils.configHandler import ConfigHandler, ConfigHandlerKey
from utils.logger import LoggerHandler
from datetime import datetime
import pytz

if __name__ == "__main__":
    # with open("large_text.txt", "w") as f:
    #     f.write("A" * (17 * 1024 * 1024))  # 7 MB de la letra "A"
    config_handler = ConfigHandler("config.ini")
    config_key = ConfigHandlerKey("key.ini")
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    key = config_key.get_key()

    colombia_tz = pytz.timezone("America/Bogota")
    now = datetime.now(colombia_tz).replace(minute=0, second=0, microsecond=0)
    hour = now.hour

    print("La hora es:", hour)

    # Se hace el llamado de la clase y se le pasan los atributos
    hoymiles = HoymileReport(
        logger=logger, config_data=config_handler, key=key, hour=int(hour))
    # hoymiles.get_list_plants()
    hoymiles.get_list_microinverters_per_plant()
    # hoymiles.get_list_plants()
    # hoymiles.get_list_microinverters_per_plant()
    # hoymiles.information_processing()
    # print(key)
