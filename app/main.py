import network, machine
from credentials import CREDENTIALS
import time
from services.json_db import Log

WLAN = network.WLAN(network.STA_IF)


def connect_to_wifi():
    _connect_to_wifi(CREDENTIALS["home"][0], CREDENTIALS["home"][1])


def _connect_to_wifi(name, password):
    WLAN.active(True)
    WLAN.connect(name, password)
    for _ in range(10):  # wait up to 10s
        if WLAN.isconnected():
            Log.add(
                "Wi-Fi",
                "connected",
                f"IP: {WLAN.ifconfig()[0]}, WLAN status: {WLAN.status()}",
            )
            return True
        time.sleep(1)
    Log.add(
        "Wi-Fi",
        "connection failed",
    )
    return False


connect_to_wifi()

from services.http_requests import http_get

http_get("https://example.com/")

import ntptime
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
    Log.add("main", "Starting main.py")

    initialize_clock()

    await initialize_from_flash()

    loop = uasyncio.new_event_loop()
    loop.create_task(_wifi_monitor())

    weather = Weather()

    Log.add("main", "Weather initialized", f"{weather.get_weather()}")

    for plant in plants:
        # schedule daily watering at 6:00 AM
        loop.create_task(schedule_daily_task(20, 5, execute_watering, (plant,)))
        # schedule daily illumination calculation at 0:30 AM
        loop.create_task(
            schedule_daily_task(0, 30, execute_iluminating, (plant, weather))
        )

    Log.add("main", "Web server started")
    await run_web_server()
    Log.add("main", "End of main.py")

    # określić jak zarządzać tym światłem?


async def _wifi_monitor():
    while True:
        if WLAN.isconnected():
            await uasyncio.sleep(30)  # sprawdzamy czy jest połączenie, co 30 sekund
        else:
            connect_to_wifi()


def initialize_clock():
    # initialize clock (will not work if no wifi)
    while True:
        try:
            ntptime.settime()
            Log.add(
                "main",
                "RTC initialized from NTP",
                f"RTC time: {machine.RTC().datetime()}",
            )
            break
        except OSError as e:
            print(e)
            Log.add(
                "main",
                "OSerror initializing RTC from NTP, reconecting to Wi-Fi",
                {"error": e},
            )
            connect_to_wifi()
            time.sleep(1)
        except Exception as e:
            print(e)
            Log.add("main", "Error initializing RTC", {"error": e})
            break


async def initialize_from_flash():
    # load all plants from flash
    try:
        plants[:] = await PlantRepo().load_all()
    except Exception as e:
        Log.add("main", "Error loading plants from flash", {"error": e})


# main()
uasyncio.run(main())
