from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Microinverter:
    DATE: str
    fecha: str
    SERIAL: str
    ID_SERVICE: int 
    ID_DEVICE: int
    # GENERATION: int
    TEMPERATURE_INVERTER: float
    VOLTAGE_1_DC: float
    VOLTAGE_2_DC: float
    VOLTAGE_3_DC: float
    VOLTAGE_4_DC: float
    CURRENT_1_DC: float
    CURRENT_2_DC: float
    CURRENT_3_DC: float
    CURRENT_4_DC: float
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
    # OPERATION_STATE: int
    VDC_5: float
    VDC_6: float
    VDC_7: float
    VDC_8: float
    VDC_9: float
    VDC_10: float
    VDC_11: float
    VDC_12: float
    VDC_13: float
    VDC_14: float
    VDC_15: float
    VDC_16: float
    VDC_17: float
    VDC_18: float
    VDC_19: float
    VDC_20: float
    IDC_5: float
    IDC_6: float
    IDC_7: float
    IDC_8: float
    IDC_9: float
    IDC_10: float
    IDC_11: float
    IDC_12: float
    IDC_13: float
    IDC_14: float
    IDC_15: float
    IDC_16: float
    IDC_17: float
    IDC_18: float
    IDC_19: float
    IDC_20: float
    F1: float
    F2: float
    F3: float
    F4: float

    def to_dict(self):
            return self.__dict__