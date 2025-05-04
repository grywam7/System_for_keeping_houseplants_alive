import machine
from ulab import numpy as np


def execute_watering(plant):
    _update_moisture(plant)
    _run_water_pump(plant)


def _update_moisture(plant):
    present_moisture = _read_moisture(plant)
    _update_moisture_history(
        plant,
        present_moisture - plant.last_measured_moisture,
        plant.last_watering_duration,
    )
    plant.last_measured_moisture = present_moisture


def _update_moisture_history(plant, moisture_change, watering_duration):
    plant.moisture_history.append(
        {"moisture_change": moisture_change, "watering_duration": watering_duration}
    )
    if len(plant.moisture_history) > 20:
        plant.moisture_history.pop(0)


def _moisture_difference(plant):
    return plant.moisture_target - plant.last_measured_moisture


# calculates the watering duration based on the moisture history
# using a polynomial regression of the second degree
def _calculate_watering(plant):
    if len(plant.moisture_history) < 3:
        return 1000
    a_index, b_index, c_index = np.polyfit(
        np.array(plant.moisture_history.get("moisture_change")),
        np.array(plant.moisture_history.get("watering_duration")),
        2,
    )
    if a_index > 0:
        return (
            a_index * _moisture_difference(plant) ** 2
            + b_index * _moisture_difference(plant)
            + c_index
        )
    else:
        return 0


def _run_water_pump(plant):
    pump = machine.Pin(plant.pump_pin, machine.Pin.OUT)
    watering_duration = _calculate_watering(plant)
    if watering_duration > 0:
        pump.on()
        machine.lightsleep(watering_duration)
        pump.off()
    plant.last_watering_duration = watering_duration


def _read_moisture(plant):
    return plant.moisture_sensor.read()
