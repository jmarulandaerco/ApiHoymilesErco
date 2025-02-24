import configparser


class ConfigHandler:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_url(self):
        return self.config.get("ENDPOINT", "URL")

    def get_plant_list(self):
        return self.config.get("ENDPOINT", "PLANT_LIST")

    def get_specified_plant(self):
        return self.config.get("ENDPOINT", "SPECIFIED_PLANT")

    def get_data_microinverter(self):
        return self.config.get("ENDPOINT", "DATA_MICROINVERTER")


class ConfigHandlerKey(ConfigHandler):
    def __init__(self, config_file):
        super().__init__(config_file)

    def get_key(self):
        return self.config.get("PASSWORD", "KEY")
