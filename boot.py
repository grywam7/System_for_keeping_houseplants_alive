# This file is executed on every boot (including wake-boot from deepsleep)
import network
import ntptime
import time


# connect to Wi-Fi
def _connect_to_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig(("192.168.1.105", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
    wlan.connect(name, password)
    time.sleep(5)
    if wlan.isconnected():
        return 0
    return 1


if _connect_to_wifi("Orange-Brzoza", "KopytkoBrzozy") == 0:
    _connect_to_wifi("Redmi", "")

# initialize clock
ntptime.settime()
