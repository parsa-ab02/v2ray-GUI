import json
import subprocess
import service


def get_socks_inbound_from_config():
    with open(service.config.config_json, "r", encoding="utf-8") as file:
        config = json.load(file)

    for inbound in config.get("inbounds", []):
        if inbound.get("tag") == "socks-in":
            return inbound

    return None

def enable_proxy():
    socks_inbound = get_socks_inbound_from_config()

    if socks_inbound is None:
        return "error: socks inbound not found"

    host = socks_inbound.get("listen", service.inbounds.DEFAULT_HOST)
    port = socks_inbound.get("port", service.inbounds.DEFAULT_SOCKS_PORT)

    subprocess.run(["gsettings", "set", "org.gnome.system.proxy", "mode", "manual"])
    subprocess.run(["gsettings", "set", "org.gnome.system.proxy.socks", "host", str(host)])
    subprocess.run(["gsettings", "set", "org.gnome.system.proxy.socks", "port", str(port)])


def disable_proxy():
    subprocess.run(["gsettings", "set", "org.gnome.system.proxy", "mode", "none"])

v2ray_process = None

def enable_v2ray():
    global v2ray_process

    v2ray_process = subprocess.Popen(["v2ray" , "run" , "-c", str(service.config.config_json)])

    enable_proxy()

def disable_v2ray():
    global v2ray_process

    if v2ray_process is not None:
        v2ray_process.terminate()
        v2ray_process = None

    disable_proxy()

def test():
    subprocess.run(["v2ray" , "test" , "-c" , str(service.config.config_json)])