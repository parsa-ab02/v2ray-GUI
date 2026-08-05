import json
import subprocess
import service
import time
import requests


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

process = None

def enable_v2ray():
    global process

    process = subprocess.Popen(["xray" , "run" , "-c", str(service.config.config_json)])

    enable_proxy()

def disable_v2ray():
    global process

    if process is not None:
        process.terminate()
        process = None

    disable_proxy()

def validator(path):
    result = subprocess.run(["xray", "run", "-test", "-c", path])
    #return result

    #needs fixing to return correct value

def ping(conf : config ,host: str, port: int):
    try:

        # config.write(conf, path)
        #
        #if(validator(path) is False):
        #    return -1
        #
        # enable_v2ray()

        start_time = time.perf_counter()

        requests.get(
            "https://www.gstatic.com/generate_204",
            proxies={
                "http":f"socks5h://{host}:{port}",
                "https":f"socks5h://{host}:{port}",
            },
            timeout=10, 
            stream=True
        )

        return (time.perf_counter()-start_time)*1000
    except requests.RequestException:
        return -1

def ping_ALL(configs_list):
    ...

    #will run ping method with mutithreading for all ts in the list
