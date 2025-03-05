import configparser

from dataclasses import dataclass, field
import urllib.parse

@dataclass
class ConfigHandler:
    # def __init__(self, config_file):
    #     self.config = configparser.ConfigParser()
    #     self.config.read(config_file)
    config_file: str    
    config: configparser.ConfigParser = field(init=False)     
    def __post_init__(self): 
        self.config = configparser.ConfigParser() 
        self.config.read(self.config_file)

    def get_url(self):
        return self.config.get("ENDPOINT", "URL")

    def get_plant_list(self):
        return self.config.get("ENDPOINT", "PLANT_LIST")

    def get_specified_plant(self):
        return self.config.get("ENDPOINT", "SPECIFIED_PLANT")

    def get_data_microinverter(self):
        return self.config.get("ENDPOINT", "DATA_MICROINVERTER")
    
    def get_retries(self):
        return self.config.get("SETTING","MAX_RETRIES")


class ConfigHandlerKey(ConfigHandler):
    def __init__(self, config_file):
        super().__init__(config_file)

    def get_key(self):
        return urllib.parse.unquote(self.config.get("PASSWORD", "KEY"))
