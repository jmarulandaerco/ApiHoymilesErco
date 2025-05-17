import configparser

from dataclasses import dataclass, field
import urllib.parse


@dataclass
class ConfigHandler:
    """
    Handles application configuration using configparser.

    Attributes:
        config_file (str): Path to the configuration file.
        config (configparser.ConfigParser): Parser instance for reading configuration.

    Methods:
        get_url() -> str:
            Returns the base API endpoint URL from the config.
        
        get_plant_list() -> str:
            Returns the endpoint for retrieving the plant list.
        
        get_specified_plant() -> str:
            Returns the endpoint for retrieving a specified plant's data.
        
        get_data_microinverter() -> str:
            Returns the endpoint for retrieving microinverter data.
        
        get_total_energy() -> str:
            Returns the endpoint for retrieving total energy data.

        get_plant_status() -> str:
            Returns the endpoint for retrieving plant status.

        get_url_token() -> str:
            Returns the endpoint for obtaining a token.
        
        get_url_enrg() -> str:
            Returns the endpoint for the energy report.
        
        get_retries() -> str:
            Returns the maximum number of retries from settings.
        
        get_log_size() -> str:
            Returns the log file size limit from settings.
        
        get_name_log() -> str:
            Returns the log file name from settings.
        
        get_json_time() -> str:
            Returns the JSON timestamp format from settings.
        
        get_interval_time() -> int:
            Returns the time interval (in seconds or minutes) from settings.
    """

    config_file: str
    config: configparser.ConfigParser = field(init=False)

    def __post_init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get_url(self) -> str:
        return self.config.get("ENDPOINT", "URL")

    def get_plant_list(self) -> str:
        return self.config.get("ENDPOINT", "PLANT_LIST")

    def get_specified_plant(self) -> str:
        return self.config.get("ENDPOINT", "SPECIFIED_PLANT")

    def get_data_microinverter(self) -> str:
        return self.config.get("ENDPOINT", "DATA_MICROINVERTER")
    
    def get_total_energy(self) -> str:
        return self.config.get("ENDPOINT", "TOTAL_ENERGY")

    def get_plant_status(self) -> str:
        return self.config.get("ENDPOINT", "PLANT_STATUS")
    
    def get_url_token(self) -> str:
        return self.config.get("ENDPOINT", "TOKEN_URL")
    
    def get_url_enrg(self) -> str:
        return self.config.get("ENDPOINT", "ENRG_URL")

    def get_retries(self) -> str:
        return self.config.get("SETTING", "MAX_RETRIES")

    def get_log_size(self) -> str:
        return self.config.get("SETTING", "LOG_SIZE")

    def get_name_log(self) -> str:
        return self.config.get("SETTING", "NAME_LOG")

    def get_json_time(self) -> str:
        return self.config.get("SETTING", "JSON_TIME")
    
    def get_interval_time(self)->int:
        return int(self.config.get("SETTING","INTERVAL_TIME"))
    


    
    

class ConfigHandlerKey(ConfigHandler):
    """
    Extends ConfigHandler to handle encrypted keys and password-related settings.

    Methods:
        get_key() -> str:
            Returns the decrypted key by URL-decoding the stored key.

        get_token_save() -> str:
            Returns the saved token from the configuration.

        get_credentials() -> str:
            Returns the stored credentials from the configuration.
    """

    def __init__(self, config_file):
        super().__init__(config_file)

    def get_key(self) -> str:
        return urllib.parse.unquote(self.config.get("PASSWORD", "KEY"))
    
    def get_token_save(self) -> str:
        return self.config.get("PASSWORD","TOKEN")
    
    def get_credentials(self) -> str:
        return self.config.get("PASSWORD","CREDENTIALS")