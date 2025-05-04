import machine
from ulab import numpy as np


class Plant:
    def __init__(
        self,
        plant_name,
        pot_index,
        pump_pin,
        moisture_sensor_pin,
        light_pins,
        plant_type,
        water_taget=1750,
        planted_on=machine.RTC().datetime()[:3],
        is_flowering=False,
        is_fruiting=False,
        moisture_history=None,
        fruiting_history=None,
        flowering_history=None,
        last_measured_moisture=0,
        last_watering_duration=0,
    ):
        self.plant_name = plant_name
        self.pot_index = pot_index
        self.pump_pin = pump_pin
        self.moisture_sensor_pin = moisture_sensor_pin
        self.light_pins = light_pins
        self.plant_type = plant_type  # TO DO, żeby zapisywać ID plant type
        self.moisture_target = water_taget
        self.planted_on = planted_on
        self.is_flowering = is_flowering
        self.is_fruiting = is_fruiting
        self.moisture_history = moisture_history if moisture_history is None else []
        self.fruiting_history = fruiting_history
        self.flowering_history = flowering_history
        self.last_measured_moisture = last_measured_moisture
        self.last_watering_duration = last_watering_duration

        # SETUP moisture sensor
        # with this setting, wery vet is 1600 (literally water in pot) and dry is 3500
        moisture_sensor = machine.ADC(machine.Pin(self.moisture_sensor_pin))
        moisture_sensor.atten(machine.ADC.ATTN_11DB)  # 0-3.3V
        moisture_sensor.width(machine.ADC.WIDTH_12BIT)  # 12-bit resolution: 0-4095
        self.moisture_sensor = moisture_sensor

    @classmethod
    def from_dict(cls, data: dict) -> "Plant":
        return cls(
            plant_name=data.get("plant_name"),
            pot_index=data.get("pot_index"),
            pump_pin=data.get("pump_pin"),
            moisture_sensor_pin=data.get("moisture_sensor_pin"),
            light_pins=data.get("light_pins"),
            water_taget=data.get("moisture_target"),
            planted_on=data.get("planted_on"),
            is_flowering=data.get("is_flowering"),
            is_fruiting=data.get("is_fruiting"),
            moisture_history=data.get("moisture_history"),
            fruiting_history=data.get("fruiting_history"),
            flowering_history=data.get("flowering_history"),
            last_measured_moisture=data.get("last_measured_moisture"),
            last_watering_duration=data.get("last_watering_duration"),
        )

    def to_dict(self):
        return {
            "plant_name": self.plant_name,
            "pot_index": self.pot_index,
            "pump_pin": self.pump_pin,
            "moisture_sensor_pin": self.moisture_sensor_pin,
            "light_pins": self.light_pins,
            "moisture_target": self.moisture_target,
            "planted_on": self.planted_on,
            "is_flowering": self.is_flowering,
            "is_fruiting": self.is_fruiting,
            "moisture_history": self.moisture_history,
            "fruiting_history": self.fruiting_history,
            "flowering_history": self.flowering_history,
            "last_measured_moisture": self.last_measured_moisture,
            "last_watering_duration": self.last_watering_duration,
        }

    def set_is_flowering(self, flowering):
        self.is_flowering = flowering
        self.update_flowering_history()

    def set_is_fruiting(self, fruiting):
        self.is_fruiting = fruiting
        self.update_fruiting_history()

    def update_flowering_history(self):
        if self.is_flowering:
            self.flowering_history.append(
                {"start": machine.RTC().datetime()[:3], "end": None}
            )
        else:
            if self.flowering_history and self.flowering_history[-1]["end"] is None:
                self.flowering_history[-1]["end"] = machine.RTC().datetime()[:3]

    def update_fruiting_history(self):
        if self.is_fruiting:
            self.fruiting_history.append(
                {"start": machine.RTC().datetime()[:3], "end": None}
            )
        else:
            if self.fruiting_history and self.fruiting_history[-1]["end"] is None:
                self.fruiting_history[-1]["end"] = machine.RTC().datetime()[:3]


# dorobić klase z rodzajem rośliny
# dorobić aplikacje webową do zarządzania roślinami
