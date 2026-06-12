import os
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_SOCKS_PORT = 1080
DEFAULT_HTTP_PORT = 1081

def is_port_free(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_free_port(host, start_port):
    port = int(start_port)

    while not is_port_free(host, port):
        port += 1

    return port

def get_inbounds():
    host = os.getenv("XRAY_HOST", DEFAULT_HOST)

    socks_port = int(os.getenv("XRAY_SOCKS_PORT", DEFAULT_SOCKS_PORT))
    http_port = int(os.getenv("XRAY_HTTP_PORT", DEFAULT_HTTP_PORT))

    socks_port = find_free_port(host, socks_port)

    if http_port == socks_port:
        http_port += 1

    http_port = find_free_port(host, http_port)

    return [
        {
            "tag": "socks-in",
            "listen": host,
            "port": socks_port,
            "protocol": "socks",
            "settings": {
                "udp": True
            }
        },
        {
            "tag": "http-in",
            "listen": host,
            "port": http_port,
            "protocol": "http",
            "settings": {}
        }
    ]