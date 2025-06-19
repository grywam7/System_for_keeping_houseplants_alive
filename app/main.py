import gc

print("Free mem at start:", gc.mem_free())

import network, machine
from credentials import CREDENTIALS
import time

WLAN = network.WLAN(network.STA_IF)


def connect_to_wifi():
    _connect_to_wifi(CREDENTIALS["home"][0], CREDENTIALS["home"][1])
    # Log.add("main", "Wi-Fi connected", {"IP": WLAN.ifconfig()[0]})


def _connect_to_wifi(name, password):
    WLAN.active(True)
    WLAN.connect(name, password)
    for _ in range(10):  # wait up to 10s
        if WLAN.isconnected():
            print(
                "Wi-Fi connected, IP:",
                WLAN.ifconfig()[0],
                "Wlan status:",
                WLAN.status(),
            )
            return True
        time.sleep(1)
    return False


from services.http_requests import http_get

connect_to_wifi()


http_get("https://example.com/")

import ntptime
from services.json_db import Log

from services.web_server import run_web_server
import uasyncio
from services.json_db import PlantRepo

# from services.json_db import PlantTypeRepo
from present_state import plants

# from present_state import plant_types
from services.task_scheduler import schedule_daily_task

from models.weather import Weather
from services.iluminating import execute_iluminating
from services.watering import execute_watering


async def main():
    print("Starting main.py...")

    initialize_clock()

    ## importing here because, when imported before wifi is connected, creates error where wifi-stack is too small

    initialize_from_flash()

    loop = uasyncio.new_event_loop()
    loop.create_task(_wifi_monitor())

    weather = Weather()

    print(weather.get_weather())
    for plant in plants:
        # schedule daily watering at 6:00 AM
        loop.create_task(schedule_daily_task(6, 0, execute_watering, (plant,)))
        # schedule daily illumination calculation at 0:30 AM
        loop.create_task(
            schedule_daily_task(0, 30, execute_iluminating, (plant, weather))
        )

    await run_web_server()
    print("Web server added to event loop")

    # określić jak zarządzać tym światłem?
    # dodać logowanie błędów


async def _wifi_monitor():
    while True:
        if WLAN.isconnected():
            print("Wi-Fi is connected")
            await uasyncio.sleep(30)  # sprawdzamy czy jest połączenie, co 30 sekund
        else:
            connect_to_wifi()


def initialize_clock():
    # initialize clock (will not work if no wifi)
    while True:
        try:
            ntptime.settime()
            break
        except OSError as e:
            print(e)
            print("Retrying to set RTC time via NTP… (trying to re-connect to Wi-Fi)")
            connect_to_wifi()
            time.sleep(1)
        except Exception as e:
            print(e)
            Log.add("main", "Error initializing RTC", {"error": e})
            break


def initialize_from_flash():
    # load all plants from flash
    try:
        plants[:] = PlantRepo().load_all()
    except Exception as e:
        Log.add("main", "Error loading plants from flash", {"error": e})


# main()
uasyncio.run(main())
