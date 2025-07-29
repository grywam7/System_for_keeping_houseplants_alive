import machine


class Plant:
    def __init__(
        self,
        plant_name,
        pot_index,
        pump_pin,
        moisture_sensor_pin,
        light_pins,
        plant_type=None,  # TO DO, do zmiany
        moisture_target=1750,
        planted_on=machine.RTC().datetime()[:3],
        is_flowering=False,
        is_fruiting=False,
        moisture_history=[],
        fruiting_history=[],
        flowering_history=[],
        last_measured_moisture=0,
        last_watering_duration=0,
    ):
        self.plant_name = plant_name
        self.pot_index = pot_index
        self.pump_pin = pump_pin
        self.moisture_sensor_pin = moisture_sensor_pin
        self.light_pins = dict(light_pins)
        self.plant_type = plant_type  # TO DO, żeby zapisywać ID plant type
        self.moisture_target = moisture_target
        self.planted_on = planted_on
        self.is_flowering = is_flowering
        self.is_fruiting = is_fruiting
        self.moisture_history = moisture_history
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
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Plant: pot_index={self.pot_index}>"

    def to_dict(self):
        data = dict(self.__dict__)
        data.pop("moisture_sensor", None)
        return data

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

    def moisture_changes(self):
        return [h["moisture_change"] for h in self.moisture_history]

    def watering_durations(self):
        return [h["watering_duration"] for h in self.moisture_history][:]
