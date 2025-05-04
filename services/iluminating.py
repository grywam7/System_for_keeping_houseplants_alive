import uasyncio
import machine


def execute_iluminating(plant, weather):
    _determine_ilumination_time(weather.get_wather())


def _determine_ilumination_time(clouds, sunrise, sunset):
    return [
        (clouds[hour] > 20 or (hour < sunrise or hour > sunset))
        for hour in range(_deterimine_ilumination_hours(sunrise, sunset))
    ]


def _deterimine_ilumination_hours(sunrise, sunset):
    if sunset - sunrise < 14:
        hour_difference = (sunset - sunrise / 2).round_up()
        start = sunrise - hour_difference
        end = sunset + hour_difference
    else:
        start = sunrise
        end = sunrise + 14

    if start > 9 or end > 23:  # w przypadku jakiegoś błedu/super długiego dnia
        start = 5
        end = 19
    return start, end + 1


async def _turn_lights_on_for(plant, time):
    ilumination_type = _determine_ilumination_type(plant)
    for color, pin in ilumination_type:
        machine.Pin(plant.light_pins[color], machine.Pin.OUT).on()

    await uasyncio.sleep(time)

    for color, pin in ilumination_type:
        machine.Pin(plant.light_pins[color], machine.Pin.OUT).off()


def _determine_ilumination_type(plant):
    if plant.is_flowering:
        return ["blue", "red"]
    elif plant.is_fruiting:
        if plant.plant_type.name == "Hot Pepper":
            return ["red", "purple"]
        return ["red"]
    else:
        return ["blue"]


async def illumination_scheduler(plant, illumination_hours):
    last_value = False
    counter = 0 - machine.RTC().datetime()[4]

    for value in illumination_hours:
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
