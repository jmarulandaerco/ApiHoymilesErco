
from App.reports import OnomondoReport
from utils.configHandler import ConfigHandler
from utils.logger import LoggerHandler


if __name__ == "__main__":
    config_handler = ConfigHandler('config.init')
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    hoymiles = OnomondoReport(logger=logger)