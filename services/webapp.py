import machine
import socket

addres = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addres)  # przypisuje adres do socketu
s.listen(1)  # pozwala na 1 połączenie
print("listening on", addres)

while True:
    client, addr = s.accept()
    print("client connected from", addr)
    client_file = client.makefile("rwb", 0)
    request = client_file.readline()
    print(request)
    if "GET / " in request or "GET /index " in request:
        with open("index.html", "rb") as f:
            response = f.read()
    elif "GET /new_plant " in request:
        with open("new_plant.html", "rb") as f:
            response = f.read()
    elif "GET /flowering " in request:
        with open("flowering.html", "rb") as f:
            response = f.read()
    elif "GET /fruiting " in request:
        with open("fruiting.html", "rb") as f:
            response = f.read()
    elif "GET /plant_params " in request:
        with open("plant_params.html", "rb") as f:
            response = f.read()
    elif "GET /delete_plant " in request:
        with open("delete_plant.html", "rb") as f:
            response = f.read()
    elif "GET /favicon.ico " in request:
        with open("favicon.ico", "rb") as f:
            response = f.read()
    else:
        response = "HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n"
    client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    client.send(response)
    client.close()
