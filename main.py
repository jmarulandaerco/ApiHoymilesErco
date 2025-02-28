from App.reports import HoymileReport
from utils.configHandler import ConfigHandler, ConfigHandlerKey
from utils.logger import LoggerHandler


if __name__ == "__main__":
    config_handler = ConfigHandler("config.ini")
    config_key = ConfigHandlerKey("key.ini")
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    key = config_key.get_key()
    #Se hace el llamado de la clase y se le pasan los atributos
    hoymiles = HoymileReport(logger=logger, config_data=config_handler, key=key)
    hoymiles.get_data_microinverters_per_plant()
    # hoymiles.get_list_microinverters_per_plant()
    #hoymiles.get_list_plants()
    #hoymiles.get_list_microinverters_per_plant()
    # hoymiles.information_processing()
    print(key)
