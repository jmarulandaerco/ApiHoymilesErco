from dataclasses import dataclass
import logging
import requests
import time
from datetime import datetime
from utils.configHandler import ConfigHandler
import pytz
import os
import json


@dataclass
class HoymileReport:
    logger: logging.Logger
    config_data: ConfigHandler
    key: str
    hour: int

    # def __init__(self, logger, config_data, key): #esto reemplaza al data class
    #     self.logger = logger
    #     self.config_data = config_data
    #     self.key = key

    def __post_init__(self):
        self.MAX_RETRIES = int(self.config_data.get_retries())

    def get_list_plants(self) -> list:
        self.logger.info("Si funciono, no soy una deshonra")
        all_plants = []
        next_page = 1

        get_plant_list = self.config_data.get_plant_list()
        key = self.key
        url = self.config_data.get_url() + get_plant_list + "key=" + key

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        try:

            name_file = "plants.json"

            if self.hour == int(self.config_data.get_json_time()):

                if os.path.exists(name_file):
                    os.remove(name_file)

                while next_page is not None:
                    data_req = {"next": next_page}
                    print(f"\n Enviando solicitud: {data_req}")

                    for attempt in range(1, self.MAX_RETRIES + 1):
                        response = requests.post(
                            url, headers=headers, json=data_req)

                        if response.status_code != 200:
                            print(
                                f"Error {response.status_code}: {response.text}")
                            self.logger.error(
                                f"Error {response.status_code}: {response}")
                            time.sleep(6)
                            continue

                        data = response.json()

                        if data["status"] != "0":
                            self.logger.error(
                                f"Error in the consult: {data['message']} with status {data['status']}")
                            time.sleep(6)
                            continue

                        print("Datos recibidos:", data)

                        stations = data.get("data", {}).get("stations", [])

                        for entry in stations:
                            all_plants.append({"id_plant": entry.get(
                                "id"), "plant_name": entry.get("station_name")})

                        next_page = data.get("data", {}).get("next", None)
                        print(f"Next page actualizado a: {next_page}")

                        if not stations or next_page is None:
                            print("No hay más estaciones o `next` no existe. bye.")
                            self.logger.info(
                                "There are no more stations available. Bye")
                            output_file = "plants.txt"
                            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            with open(output_file, "a", encoding="utf-8") as plants_file:
                                plants_file.write(current_date + '\n')
                                for plant in all_plants:
                                    plants_file.write(
                                        f'{plant["id_plant"]}, {plant["plant_name"]}\n')
                                    print(plant)
                                plants_file.write('\n')

                            with open(name_file, "w", encoding="utf-8") as file:
                                json.dump(all_plants, file, indent=4,
                                          ensure_ascii=False)

                            return all_plants

                        time.sleep(6)
                        break

                    else:
                        print("Se alcanzó el número máximo de intentos sin éxito.")
                        self.logger.error(
                            f"Unable to consult the list of plants, maximum number of attempts made. Max retries = {self.MAX_RETRIES}")
                        return []
            else:
                if os.path.exists(name_file):
                    with open("plants.json", "r", encoding="utf-8") as file:
                        return json.load(file)  # No escapa caracteres Unicode

                else:
                    return []

        except Exception as ex:
            self.logger.error(f"Error while asking for plants {ex}")
            return []

    def get_list_microinverters_per_plant(self) -> list:

        all_microinverters = []
        micros_per_plant = self.config_data.get_specified_plant()
        key = self.key
        url = self.config_data.get_url() + micros_per_plant + "key=" + key
        print(url)

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        all_plants = self.get_list_plants()
        print(all_plants)
        try:

            name_file = "micros_id.json"

            if self.hour == int(self.config_data.get_json_time()):

                if os.path.exists(name_file):
                    os.remove(name_file)

                for plant in all_plants:
                    proy_id = plant.get("id_plant")
                    print("Plants ID", proy_id)

                    # if not plant:
                    #     self.logger.info("There are no more plants IDs.")
                    #     break

                    data_req = {"id": proy_id}
                    for attempt in range(1,  self.MAX_RETRIES + 1):
                        response = requests.post(
                            url, headers=headers, json=data_req)

                        if response.status_code != 200:
                            print(
                                f"Error {response.status_code}: {response.text}")
                            self.logger.error(
                                f"Error {response.status_code}: {response}")
                            time.sleep(6)
                            continue

                        data = response.json()

                        if data["status"] != "0":
                            # print("Error en la consulta:", data["message"])
                            self.logger.error(
                                f"Error in the consult: {data['message']} with status {data['status']}")
                            time.sleep(6)
                            continue

                        time.sleep(6)
                        break
                    else:
                        print("Se alcanzó el número máximo de intentos sin éxito.")
                        self.logger.error(
                            f"Unable to consult the list of plants, maximum number of attempts made. Max retries ={self.MAX_RETRIES}")
                        return []

                    micro_datas = list({item.get("mi_sn") for item in data.get(
                        "data", {}).get("micro_datas", [])})

                    print("Lista de microinversores: ", micro_datas)

                    all_microinverters.append({"id_plant": proy_id, "plant_name": plant.get(
                        "plant_name"), "micros_id": micro_datas})

                with open(name_file, "w", encoding="utf-8") as file:
                    json.dump(all_microinverters, file,
                              indent=4, ensure_ascii=False)

                print("SERIALES DE LOS MICROS: ", all_microinverters)
                return all_microinverters

            else:
                if os.path.exists(name_file):
                    with open("micros_id.json", "r", encoding="utf-8") as file:
                        print(json.load(file))  # No escapa caracteres Unicode
                else:
                    return []

        except Exception as ex:
            self.logger.error(f"Error while asking for plants {ex}")
            return []

    def get_data_microinverters_per_plant(self) -> list:
        all_data_microinverters = []
        current_date = datetime.now()
        current_date_formatted = current_date.strftime("%Y-%m-%d")
        micros_per_plant = self.config_data.get_data_microinverter()
        key = self.key
        url = self.config_data.get_url() + micros_per_plant + "key=" + key
        print(url)
        print("la fecha actual es:", current_date_formatted)
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        all_microinverters = self.get_list_microinverters_per_plant()
        try:
            for plants in all_microinverters:
                for microinverters in plants.get("micros_id"):
                    print("Microinversores obtenidos", microinverters)
                    data_req = {
                        "station_id": plants.get("id_plant"),
                        "date": current_date_formatted,
                        "sn": microinverters
                    }
                    for attempt in range(1, self.MAX_RETRIES + 1):

                        response = requests.post(
                            url, headers=headers, json=data_req)
                        print(f"informacion micros: {response.json()}")
                        time.sleep(6)
                        break
                    else:
                        print("Se alcanzó el número máximo de intentos sin éxito.")
                        self.logger.error(
                            f"Unable to consult the list of plants, maximum number of attempts made. Max retries ={self.MAX_RETRIES}")
                        return []
        except Exception as ex:
            self.logger.error(f"Error while asking for plants {ex}")
            return []

    def information_processing(self) -> None:
        self.logger.info(
            f"Error en AnotherClass{self.config_data.get_url()}"
        )
