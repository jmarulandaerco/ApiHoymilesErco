from dataclasses import dataclass
import logging
import requests
import time
from datetime import datetime

from utils.configHandler import ConfigHandler


@dataclass
class HoymileReport:
    logger: logging.Logger
    config_data: ConfigHandler
    key: str

    # def __init__(self, logger, config_data, key): #esto reemplaza al data class
    #     self.logger = logger
    #     self.config_data = config_data
    #     self.key = key

    def get_list_plants(self) -> list:
        all_plants = [] 
        next_page = 1  

        get_plant_list = self.config_data.get_plant_list()
        key = self.key
        url = self.config_data.get_url() + get_plant_list + "key=" + key
        #url = f"https://wapi.hoymiles.com{get_plant_list}key={key}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
        try:

            while next_page is not None:  
                data_req = {"next": next_page}  
                print(f"\n Enviando solicitud: {data_req}")

                response = requests.post(url, headers=headers, json=data_req)

                if response.status_code != 200:
                    print(f"Error {response.status_code}: {response.text}")
                    self.logger.error(f"Error {response.status_code}: {response}")
                    break  

                data = response.json()
                
                if data["status"] != "0":
                    # print("Error en la consulta:", data["message"])
                    self.logger.error(f"Error in the consult: {data['message']}")
                    break

                print("Datos recibidos:", data)

                # Obtener lista de estaciones
                stations = data.get("data", {}).get("stations", [])
                
                for entry in stations:
                    
                #ids = [station.get("id") for station in data.get("data", {}).get("stations", [])]
                    all_plants.append({"id_plant": entry.get("id"), "plant_name":entry.get("station_name")})
                #all_plants.extend(stations)  # Agregar solo si hay estaciones
                #proy_id.extend(ids)
                #print("ESTOS SON LOS IDS DE LAS PLANTAS:", proy_id)

                
                next_page = data.get("data", {}).get("next", None)  # Si no hay "next", devuelve None
                
                print(f"Next page actualizado a: {next_page}")

                
                if not stations or next_page is None:
                    print("No hay más estaciones o `next` no existe. bye.")
                    self.logger.info("There are no more stations available. Bye")
                    break
                
                time.sleep(6)

            print(f"\n Total de estaciones obtenidas: {len(all_plants)}")
            print("Lista filtrada: ", all_plants)
        
        except Exception as ex: 
            self.logger.error(f"Error while asking for plants {ex}")
            return []

        return all_plants


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

        try:
             
            for plant in all_plants:
                proy_id = plant.get("id_plant")
                print("Plants ID", proy_id)

                if not plant:
                    self.logger.info("There are no more plants IDs.")
                    break

                data_req = {"id": proy_id} 
                response = requests.post(url, headers=headers, json=data_req)

                if response.status_code != 200:
                        print(f"Error {response.status_code}: {response.text}")
                        self.logger.error(f"Error {response.status_code}: {response}")
                        break  

                data = response.json()
                
                if data["status"] != "0":
                        # print("Error en la consulta:", data["message"])
                        self.logger.error(f"Error in the consult: {data['message']}")
                        break
                
                time.sleep(6)

                micro_datas = {item.get("mi_sn") for item in data.get("data", {}).get("micro_datas", [])}

                print("Lista de microinversores: ", micro_datas)

                all_microinverters.append({"id_plant": proy_id, "plant_name": plant.get("plant_name"), "micros_id": micro_datas})
        
        except Exception as ex:
            self.logger.error(f"Error while asking for plants {ex}")
            return []
        
        print("SERIALES DE LOS MICROS: ", all_microinverters)

        return all_microinverters

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

        # { 
        # "station_id": 1325870 , 
        # "date": "2025-02-25", 
        # "sn": "106154401367" }

    def information_processing(self) -> None:
        self.logger.info(
            f"Error en AnotherClass{self.config_data.get_url()}"
        )
