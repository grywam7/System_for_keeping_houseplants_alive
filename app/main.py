import machine
import time
import network
import socket
import ssl
import ntptime
from services.json_db import PlantRepo

# from services.json_db import PlantTypeRepo
from present_state import PLANTS
from present_state import PLANT_TYPES

# from task_scheduler import TaskScheduler
from services.web_server import run_web_server
from credentials import CREDENTIALS

ILUMINATION_START = 6
ILUMINATION_DURATION = 14


# connect to Wi-Fi
def _connect_to_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig(("192.168.1.153", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
    wlan.connect(name, password)
    # wait up to 10s
    for _ in range(20):
        if wlan.isconnected():
            print("Wi-Fi connected, IP:", wlan.ifconfig()[0])
            return True
        time.sleep(0.5)
    return False


async def initialize_from_flash():
    # load all plants from flash
    try:
        PLANTS[:] = await PlantRepo().load_all()
    except Exception as e:
        print("Error loading plants from flash:", e)

    # # load all plant types from flash
    # try:
    #     PLANT_TYPES[:] = await PlantTypeRepo().load_all()
    # except Exception as e:
    #     print("Error loading plant types from flash:", e)


# while not network.WLAN(network.STA_IF).isconnected():
_connect_to_wifi(CREDENTIALS["home"][0], CREDENTIALS["home"][1])
# _connect_to_wifi(CREDENTIALS["mobile"][0], CREDENTIALS["mobile"][1])

print(network.WLAN(network.STA_IF).ipconfig("addr4"))
# initialize clock (will not work if no wifi)
while True:
    try:
        ntptime.settime()
        break
    except:
        time.sleep(1)

initialize_from_flash()


# wifi_monitor()
# TaskScheduler.start()

run_web_server()


# zainicjować roślinke ? ale przez api
# codziennie o 1 wołać calculate ilumination hours
# a następnie konsultować to z roślinką żęby określić czy potrzebuje niebieskie czy czernowne światło
# określić jak zarządzać tym światłem?

# PRIVATE METHODS

# async def wifi_monitor():
