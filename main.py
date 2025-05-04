import machine
import time
import network
import socket
import ssl
import ntptime

ILUMINATION_START = 6
ILUMINATION_DURATION = 14


# while True:
def main():
    _connect_to_wifi("Orange-Brzoza", "KopytkoBrzozy")
    _connect_to_wifi("AGH-5", "dAZNmmwh4x")
    _calculate_ilumination_hours()


# zainicjować roślinke ? ale przez api
# codziennie o 1 wołać calculate ilumination hours
# a następnie konsultować to z roślinką żęby określić czy potrzebuje niebieskie czy czernowne światło
# określić jak zarządzać tym światłem?


# PRIVATE METHODS


def _connect_to_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig(("192.168.1.105", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(name, password)
        while not wlan.isconnected():
            machine.idle()
    print("network config:", wlan.ipconfig("addr4"))
