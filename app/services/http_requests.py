import socket
import ssl


async def http_get(url: str, https: bool = False):
    _, _, host, path = url.split("/", 3)
    if https:
        addr = socket.getaddrinfo(host, 443)[0][-1]
    else:
        addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    if https:
        s = ssl.wrap_socket(s, server_hostname=host)
    s.write(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    data = s.read()
    s.close()
    if data:
        return data.decode("utf8")
    else:
        return {}
