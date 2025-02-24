from App.reports import OnomondoReport
from utils.configHandler import ConfigHandler, ConfigHandlerKey
from utils.logger import LoggerHandler


if __name__ == "__main__":
    config_handler = ConfigHandler("config.ini")
    config_key = ConfigHandlerKey("key.ini")
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    key = config_key.get_key()
    hoymiles = OnomondoReport(logger=logger, config_data=config_handler, key=key)
    # hoymiles.get_data_microinverters_per_plant()
    # hoymiles.get_list_microinverters_per_plant()
    hoymiles.get_list_plants()
    # hoymiles.information_processing()
    print(key)
