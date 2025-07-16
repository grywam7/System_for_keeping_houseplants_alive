import socket
import ssl
from services.json_db import Log


def http_get(url: str):
    https, _, host, path = url.split("/", 3)
    if https == "https:":
        addr = socket.getaddrinfo(host, 443)[0][-1]
    else:
        addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    if https == "https:":
        s = ssl.wrap_socket(s, server_hostname=host)
    s.write(
        bytes(
            "GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host),
            "utf8",
        )
    )
    data = s.read()
    s.close()
    Log.add("http_get", "Request sent", {"url": url, "response_length": len(data)})
    if data:
        return data.decode("utf8")
    else:
        return {}
