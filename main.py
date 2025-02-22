
from App.reports import OnomondoReport
from utils.configHandler import ConfigHandler
from utils.logger import LoggerHandler


if __name__ == "__main__":
    config_handler = ConfigHandler('config.ini')
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    hoymiles = OnomondoReport(logger=logger,config_data=config_handler)
    hoymiles.get_data_microinverters_per_plant()
    hoymiles.get_list_microinverters_per_plant()
    hoymiles.get_list_plants()
    hoymiles.information_processing()