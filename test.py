import machine
import time
import network
import socket
import ssl
import ntptime


def _connect_to_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    wlan = network.WLAN()
    wlan.active(True)
    wlan.ifconfig(("192.168.1.105", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(name, password)
        while not wlan.isconnected():
            machine.idle()
    print("network config:", wlan.ipconfig("addr4"))


wifi = _connect_to_wifi("Orange-Brzoza", "KopytkoBrzozy")

print(wifi)

addres = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addres)  # przypisuje adres do socketu
s.listen(1)  # pozwala na 1 połączenie
print("listening on", addres)


html = """<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8" />
    <title>Plant Care App Interface</title>
    <!-- <link rel="icon" type="image/svg" href="/favicon.ico" /> -->
    <style>
    </style>
</head>

<body>
    <h1>Select operation:</h1>
    <ul>
        <li>-> <a href="/new_plant">add new plant</a></li>
        <li>-> update plant</li>
        <ul>
            <li>-> <a href="/flowering">set flowering</a></li>
            <li>-> <a href="/fruiting">set fruiting</a></li>
            <li>-> <a href="/plant_params">change other, plant parameters</a></li>
        </ul>
        <li>-> <a href="/delete_plant">delete plant</a></li>
    </ul>
</body>

</html>
"""


while True:
    client, addr = s.accept()
    print("client connected from", addr)
    client_file = client.makefile("rwb", 0)
    while True:
        line = client_file.readline()
        print(line)
        if not line or line == b"\r\n":
            break
    response = html
    client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    client.send(response)
    client.close()
