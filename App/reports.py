from dataclasses import dataclass
import logging
import requests
import time
from datetime import datetime
from App.models.microinverters import Microinverter
from utils.configHandler import ConfigHandler
import pytz
import os
import json

@dataclass
class HoymileReport:

    """
    Fetching data from hoymiles API.

    Attributes:
        LOG_FILE (str): Path to the log file.
        MAX_LOG_SIZE (int): Maximum allowed log file size in bytes.
        logger (logging.Logger): Logger instance for saving class logs.
        config_data (ConfigHandler): Config instance for getting query settings.
        key (str): API key for fetching data from Hoymiles API.
        hour (int): Current date for fetching data.

    Methods:
         __post_init__(): Initialize self.MAX_RETRIES.
        get_list_plants() -> list: Gets the list of the avalable plants.
        get_list_microinverters_per_plant() -> list: Gets the list of the asigned microinverters per plant.
        get_data_microinverters_per_plant() -> list: Gets the data of each microinverter per plant.
        __get_total_energy() -> str: Get the total energy of the plant.
        __get_plant_status() -> dict: Get the operation states of the plant.

    """

    logger: logging.Logger
    config_data: ConfigHandler
    key: str
    hour: int

    def __post_init__(self):
        self.MAX_RETRIES = int(self.config_data.get_retries())

    def get_list_plants(self) -> list:
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
                            print("No hay más estaciones o `next` no existe.")
                            # self.logger.info(
                            #     "There are no more stations available")
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
                            self.logger.error(
                                f"Error in the consult: {data['message']} with status {data['status']} in the plant with id: {proy_id}")
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
                        return json.load(file)  # No escapa caracteres Unicode
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
        print("hola")
        all_microinverters = self.get_list_microinverters_per_plant()
        print(all_microinverters)

        try:
            for plants in all_microinverters:
                data_microinverters = []
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
                        if response.status_code != 200:
                            # print(
                            #     f"Error {response.status_code}: {response.text}")
                            self.logger.error(
                                f"Error {response.status_code}: {response}")
                            time.sleep(6)
                            continue

                        data = response.json()

                        if data["status"] != "0":
                            # print("Error en la consulta:", data["message"])
                            self.logger.error(
                                f"Error in the consult: {data['message']} with status {data['status']} in the plant with id: {plants.get('id_plant')}")
                            time.sleep(6)
                            continue

                        time.sleep(6)
                        data_microinverters.append(
                            {"id_micro": microinverters, "generation": data.get("data")})
                        break
                    else:
                        print("Se alcanzó el número máximo de intentos sin éxito.")
                        self.logger.error(
                            f"Unable to consult the list microinverters per plant, maximum number of attempts made. Max retries ={self.MAX_RETRIES}")
                        return []

                total_energy_per_plant = self.__get_total_energy(
                    plants.get("id_plant"))
                plant_status = self.__get_plant_status(plants.get("id_plant"))

                all_data_microinverters.append({"id_plant": plants.get("id_plant"), "name_plant": plants.get(
                    "plant_name"), "total_energy": total_energy_per_plant, "plant_status": plant_status, "data_inverters": data_microinverters})

            with open('data.json', "w", encoding="utf-8") as file:
                json.dump(all_data_microinverters, file,
                          indent=4, ensure_ascii=False)

            return all_data_microinverters
        
        except Exception as ex:
            self.logger.error(
                f"Error while asking for microinverters data {ex}")
            return []

    def __get_total_energy(self, id_plant: int) -> str:

        url_total_energy_plant = self.config_data.get_total_energy()
        key = self.key
        url = self.config_data.get_url() + url_total_energy_plant + "key=" + key
        print(url)

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        data_req = {"station_id": id_plant}

        try:

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
                    f"Unable to consult the total energy, maximum number of attempts made. Max retries ={self.MAX_RETRIES}")
                return None

            total_energy_plant = data.get("data")

            print("Energía total de la planta: ", total_energy_plant)

        except Exception as ex:
            self.logger.error(
                f"Error while asking for total energy per plant {ex}")
            return None

        return total_energy_plant

    def __get_plant_status(self, id_plant: int) -> dict:

        url_plant_status = self.config_data.get_plant_status()
        key = self.key
        url = self.config_data.get_url() + url_plant_status + "key=" + key
        print(url)

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        data_req = {"id": id_plant}

        try:

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
                    f"Unable to consult the operation state of the plant, maximum number of attempts made. Max retries ={self.MAX_RETRIES}")
                return None

            plant_status = data.get("data")

            print("Status de la planta: ", plant_status)

        except Exception as ex:
            self.logger.error(
                f"Error while asking for the operation state of the plant {ex}")
            return None

        return plant_status

    def information_processing(self) -> None:
    
        data_total= self.get_aux()
        print(data_total)
       
        json_string = json.dumps(self.create_payload(data_total,1), indent=4)  # `indent=4` para hacerlo legible
       
        with open('datoslala.json', 'w') as archivo_json:
        # Usa json.dump() para escribir el diccionario en el archivo
            archivo_json.write(json_string)
        print("Diccionario guardado como datos.json")

    def create_payload(self,plant_data: list[dict],id_service: int):
        
        data_plant = []
        payload_plant = []

        for plant in plant_data:
            generation = plant.get("total_energy")
            id_plant = plant.get("id_plant")
            plant_status = plant.get("plant_status")

            for microinverter in plant.get("data_inverters"):
                if microinverter.get("generation") and microinverter.get("generation") != []:
                    last_generation = microinverter.get("generation")[0]

                    date_obj = datetime.now()
                    today_str = date_obj.strftime("%Y-%m-%d")
                    date_str = f"{today_str} {last_generation['time']}:00"
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    date_str_formatted = date_obj.strftime("%Y-%m-%d %H:%M:%S")

                    alarms = {
                        "OFFLINE": plant_status.get("offline"),
                        "UNSTABLE": plant_status.get("unstable"),
                        "UMATCHED": plant_status.get("umatched"),
                        "MICROINVERT_WARN": plant_status.get("mi_warn"),
                        "GRID_WARN": plant_status.get("g_warn"),
                        "LAST_AT": date_str_formatted
                    }

                    ac_data = last_generation.get("ac")
                    temp_microinverter = ac_data.get("temp")
                    grid_freq = ac_data.get("freq")
                    voltage_1_ac = ac_data.get("ua")
                    voltage_2_ac = ac_data.get("ub")
                    voltage_3_ac = ac_data.get("uc")

                    dc_data = last_generation.get("dc")

                    dc_voltage = [0.0]*8
                    dc_current = [0.0]*8

                    print(dc_voltage)
                    print(dc_current)

                    for i,x in enumerate(dc_data):
                        dc_voltage[i] = x.get("u")
                        dc_current[i] = x.get("i")


                else:
                    date_obj = datetime.now()
                    date_str_formatted = date_obj.strftime("%Y-%m-%d %H:%M:%S")

                    ac_data = {"ua": 0.0, "ub": 0.0, "uc": 0.0, "temp": 0.0}
                    voltage_dc = [0.0] * 8
                    current_dc = [0.0] * 8
                    temp_microinverter = 0.0
                    grid_freq = 0.0
                    voltage_1_ac = 0.0
                    voltage_2_ac = 0.0
                    voltage_3_ac = 0.0

                    #current_1_ac = generation/p

                    alarms = {
                        "OFFLINE": plant_status.get("offline"),
                        "UNSTABLE": plant_status.get("unstable"),
                        "UMATCHED": plant_status.get("umatched"),
                        "MICROINVERT_WARN": plant_status.get("mi_warn"),
                        "GRID_WARN": plant_status.get("g_warn"),
                        "LAST_AT": date_str_formatted
                    }
        
                payload = Microinverter(
                    DATE = date_str_formatted,
                    ID_DEVICE = microinverter.get("id_micro"),
                    TEMPERATURE_INVERTER = temp_microinverter,
                    VOLTAGE_1_DC = dc_voltage[0],
                    VOLTAGE_2_DC = dc_voltage[1],
                    VOLTAGE_3_DC = dc_voltage[2],
                    VOLTAGE_4_DC = dc_voltage[3],
                    VOLTAGE_5_DC = dc_voltage[4],
                    VOLTAGE_6_DC = dc_voltage[5],
                    VOLTAGE_7_DC = dc_voltage[6],
                    VOLTAGE_8_DC = dc_voltage[7],
                    CURRENT_1_DC = dc_current[0],
                    CURRENT_2_DC = dc_current[1],
                    CURRENT_3_DC = dc_current[2],
                    CURRENT_4_DC = dc_current[3],
                    CURRENT_5_DC = dc_current[4],
                    CURRENT_6_DC = dc_current[5],
                    CURRENT_7_DC = dc_current[6],
                    CURRENT_8_DC = dc_current[7],
                    VOLTAGE_1_AC = voltage_1_ac,
                    VOLTAGE_2_AC = voltage_2_ac,
                    VOLTAGE_3_AC = voltage_3_ac,
                    CURRENT_1_AC = 0.0,
                    CURRENT_2_AC = 0.0,
                    CURRENT_3_AC = 0.0,
                    IRRADIANCE = 0.0,
                    TEMPERATURE_PANEL = 0.0,
                    TEMPERATURE_ENVIRONMENT = 0.0,
                    TEMPERATURE_PCB = 0.0,
                    TYPE_INVERTER = 9, #PREGUNTAR CUAL ES
                    POWER_FACTOR = 0.0,
                    TYPE_DEVICE = 0.0,
                    POWER_SNAPSHOT = 0.0,
                    GRID_FREQUENCY = grid_freq,
                    HEATSINK_TEMPERATURE = 0.0,
                    APPARENT_POWER = 0.0,
                    REACTIVE_POWER = 0.0,
                    WIND_SPEED = 0.0,
                    WIND_DIRECTION = 0.0,
                    HUMIDITY = 0.0,
                    F1 = 0.0,
                    F2 = 0.0,
                    F3 = 0.0,
                    F4 = 0.0,
                )
            
                data_plant.append(payload.__dict__)

            payload_plant.append({
                "GENERATION": generation,
                "ID_PLANT" : id_plant,
                "DATE_GENERATION" : date_str_formatted,
                "STATE_OPERATION": alarms,
                "INFORMATION_MICRO_INVERTERS": data_plant
            })

            data_plant = []


        return payload_plant

    def get_aux(self):
        data = self.get_data_microinverters_per_plant()
        print(data)
        for plant in data:
            plant["data_inverters"] = sorted(plant["data_inverters"], key=lambda x: x["id_micro"], reverse=True)

            for microinverters in plant["data_inverters"]:
                generation = microinverters.get("generation",[])
                
                if generation:
                    latest_gen = max(generation, key=lambda gen: datetime.strptime(gen["time"], '%H:%M'))
                    microinverters["generation"] = [latest_gen]
                
                else:
                    microinverters["generation"] = []

        with open('data2.json', "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
 
        return data

