from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Microinverter:
    DATE: str
    ID_DEVICE: int 
    TEMPERATURE_INVERTER: float
    VOLTAGE_1_DC: float
    VOLTAGE_2_DC: float
    VOLTAGE_3_DC: float
    VOLTAGE_4_DC: float
    VOLTAGE_5_DC: float
    VOLTAGE_6_DC: float
    VOLTAGE_7_DC: float
    VOLTAGE_8_DC: float
    CURRENT_1_DC: float
    CURRENT_2_DC: float
    CURRENT_3_DC: float
    CURRENT_4_DC: float
    CURRENT_5_DC: float
    CURRENT_6_DC: float
    CURRENT_7_DC: float
    CURRENT_8_DC: float
    VOLTAGE_1_AC: float
    VOLTAGE_2_AC: float
    VOLTAGE_3_AC: float
    CURRENT_1_AC: float
    CURRENT_2_AC: float
    CURRENT_3_AC: float
    IRRADIANCE: float
    TEMPERATURE_PANEL: float
    TEMPERATURE_ENVIRONMENT: float
    TEMPERATURE_PCB: float
    TYPE_INVERTER: int
    POWER_FACTOR: float
    TYPE_DEVICE: int
    POWER_SNAPSHOT: float
    GRID_FREQUENCY: float
    HEATSINK_TEMPERATURE: float
    APPARENT_POWER: float
    REACTIVE_POWER: float
    WIND_SPEED: float
    WIND_DIRECTION: float
    HUMIDITY: float
    F1: float
    F2: float
    F3: float
    F4: float

    def to_dict(self):
            return self.__dict__