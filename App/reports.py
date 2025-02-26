from dataclasses import dataclass
import logging

from utils.configHandler import ConfigHandler


@dataclass
class OnomondoReport:
    logger: logging.Logger
    config_data: ConfigHandler
    key: str

    # def __init__(self, logger, config_data, key): #esto reemplaza al data class
    #     self.logger = logger
    #     self.config_data = config_data
    #     self.key = key

    def __get_list_plants(self) -> list:
        self.logger.info(
            f"Error en el INTENTO{self.config_data.get_data_microinverter()}"
        )

    def get_list_microinverters_per_plant(self) -> list:
        self.__get_list_plants()
        self.logger.info(
            f"Error en AnotherClass{self.config_data.get_plant_list()}"
        )

    def get_data_microinverters_per_plant(self) -> list:
        self.logger.info(
            f"Error en AnotherClass{self.config_data.get_specified_plant()}"
        )

    def information_processing(self) -> None:
        self.logger.info(
            f"Error en AnotherClass{self.config_data.get_url()}"
        )
