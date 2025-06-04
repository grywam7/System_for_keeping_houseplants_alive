import machine
import time
import network
from services.web_server import run_web_server
from credentials import CREDENTIALS
import ntptime
from services.json_db import Log

def connect_to_wifi():
    if not _connect_to_wifi(CREDENTIALS["home"][0], CREDENTIALS["home"][1]):
        _connect_to_wifi(CREDENTIALS["mobile"][0], CREDENTIALS["mobile"][1])
    Log.add('main',"Wi-Fi connected", {'IP': network.WLAN(network.STA_IF).ifconfig()[0]})


async def _wifi_monitor():
    while True:
        if network.WLAN(network.STA_IF).isconnected():
            uasyncio.sleep(30)  # sprawdzamy czy jest połączenie, co 30 sekund
        else:
            connect_to_wifi()


def _connect_to_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # wlan.ifconfig(("192.168.1.153", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
    wlan.connect(name, password)

    for _ in range(10):  # wait up to 10s
        if wlan.isconnected():
            print("Wi-Fi connected, IP:", wlan.ifconfig()[0])
            return True
        time.sleep(1)
    return False


async def initialize_from_flash():
    # load all plants from flash
    try:
        plants[:] = await PlantRepo().load_all()
    except Exception as e:
        Log.add('main', 'Error loading plants from flash', {'error': e})


_connect_to_wifi(CREDENTIALS["home"][0], CREDENTIALS["home"][1])

# initialize clock (will not work if no wifi)
while True:
    try:
        ntptime.settime()
        break
    except OSError:
        connect_to_wifi()
        time.sleep(1)
    except Exception as e:
        Log.add('main', 'Error initializing RTC', {'error': e})

## importing here because, when imported before wifi is connected, creates error where wifi-stack is too small
import uasyncio
from services.json_db import PlantRepo

# from services.json_db import PlantTypeRepo
from present_state import plants

# from present_state import plant_types
from services.task_scheduler import schedule_daily_task

from models.weather import Weather
from services.iluminating import execute_iluminating
from services.watering import execute_watering

uasyncio.run(initialize_from_flash())

uasyncio.create_task(_wifi_monitor())

weather = Weather()


for plant in plants:
    # schedule daily watering at 6:00 AM
    uasyncio.create_task(schedule_daily_task(6, 0, execute_watering, (plant,)))
    # schedule daily illumination calculation at 0:30 AM
    uasyncio.create_task(
        schedule_daily_task(0, 30, execute_iluminating, (plant, weather))
    )

run_web_server()

# określić jak zarządzać tym światłem?
# dodać logowanie błędów
