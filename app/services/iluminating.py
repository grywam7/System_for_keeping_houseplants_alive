import uasyncio
import machine
import math
from models.plant import Plant
from models.weather import Weather


async def execute_iluminating(plant: Plant, weather: Weather):
    await _illumination_scheduler(plant, weather)


def _deterimine_ilumination_hours(sunrise, sunset):
    if sunset - sunrise < 14:
        hour_difference = math.ceil((sunset - sunrise) / 2)
        start = sunrise - hour_difference
        end = sunset + hour_difference
    else:
        start = sunrise
        end = sunrise + 14

    # w przypadku jakiegoś super długiego dnia/błędnych danych z api
    if start > 9 or end > 23:
        start = 5
        end = 19
    return start, end + 1


def _determine_ilumination_time(sunshine, sunrise, sunset):
    return [
        (sunshine[hour] < 3300 or (hour < sunrise or hour > sunset))
        for hour in range(_deterimine_ilumination_hours(sunrise, sunset))
    ]


# def _determine_ilumination_type(plant):
#     if plant.is_flowering:
#         return ["blue", "red"]
#     elif plant.is_fruiting:
#         if plant.plant_type.name == "Hot Pepper":
#             return ["red", "purple"]
#         return ["red"]
#     else:
#         return ["blue"]
# def _determine_ilumination_type():
#     return ["red", "blue"]


async def _turn_lights_on_for(plant, time):
    # ilumination_type = _determine_ilumination_type()
    # for color in ilumination_type:
    machine.Pin(plant.light_pins, machine.Pin.OUT).on()

    await uasyncio.sleep(time)

    # for color in ilumination_type:
    machine.Pin(plant.light_pins, machine.Pin.OUT).off()


async def _illumination_scheduler(plant, weather):
    last_value = False
    counter = 0 - machine.RTC().datetime()[4]

    for value in _determine_ilumination_time(**weather.get_weather()):
        if value == last_value:
            counter += 1
        else:
            current_minute, current_second = machine.RTC().datetime()[5:7]
            time = 3600 - (current_minute * 60 + current_second) + counter * 3600
            if time > 0:
                if value:
                    await _turn_lights_on_for(plant, time)
                else:
                    await uasyncio.sleep(time)

            counter = 1
            last_value = value
