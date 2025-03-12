import configparser

from dataclasses import dataclass, field
import urllib.parse


@dataclass
class ConfigHandler:
    """
    Handles application configuration using configparser.

    Attributes:
        config_file (str): Path to the configuration file.
        config (configparser.ConfigParser): ConfigParser instance.

    Methods:
        get_url() -> str: Returns the API endpoint URL.
        get_plant_list() -> str: Returns the plant list endpoint.
        get_specified_plant() -> str: Returns the specified plant endpoint.
        get_data_microinverter() -> str: Returns the microinverter data endpoint.
        get_retries() -> str: Returns the maximum number of retries.
        get_log_size() -> str: Returns the log file size limit.
        get_name_log() -> str: Returns the log file name.
    """
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
        return self.config.get("SETTING", "MAX_RETRIES")

    def get_log_size(self):
        return self.config.get("SETTING", "LOG_SIZE")

    def get_name_log(self):
        return self.config.get("SETTING", "NAME_LOG")

    def get_json_time(self):
        return self.config.get("SETTING", "JSON_TIME")


class ConfigHandlerKey(ConfigHandler):
    """
    Extends ConfigHandler to handle encrypted keys.

    Methods:
        get_key() -> str: Returns the decrypted key.
    """

    def __init__(self, config_file):
        super().__init__(config_file)

    def get_key(self):
        return urllib.parse.unquote(self.config.get("PASSWORD", "KEY"))
