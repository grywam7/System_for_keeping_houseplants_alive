import machine
import time
import network
import socket
import ssl
import ntptime
from services.json_db import PlantRepo

# from services.json_db import PlantTypeRepo
from present_state import PLANTS
# from present_state import PLANT_TYPES

# from task_scheduler import TaskScheduler
from services.web_server import run_web_server

ILUMINATION_START = 6
ILUMINATION_DURATION = 14


# while True:
def main():
    PLANTS[:] = PlantRepo.load_all()
    # PLANT_TYPES[:] = PlantTypeRepo.load_all()
    # wifi_monitor()
    # TaskScheduler.start()
    run_web_server()


# zainicjować roślinke ? ale przez api
# codziennie o 1 wołać calculate ilumination hours
# a następnie konsultować to z roślinką żęby określić czy potrzebuje niebieskie czy czernowne światło
# określić jak zarządzać tym światłem?

# PRIVATE METHODS

# async def wifi_monitor():
