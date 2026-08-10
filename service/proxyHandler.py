from service.proxy import Proxy

from protocol.vless import VlessProxy
from protocol.vmess import VmessProxy
from protocol.trojan import TrojanProxy
from protocol.shadowsocks import ShadowsocksProxy
from protocol.hysteria2 import Hysteria2Proxy
from protocol.http import HttpProxy

PROTOCOL_REGISTRY = {
    "vless": VlessProxy,
    "vmess": VmessProxy,
    "trojan": TrojanProxy,
    "ss": ShadowsocksProxy,
    "shadowsocks": ShadowsocksProxy,
    "hysteria2": Hysteria2Proxy,
    "hy2": Hysteria2Proxy,
    "http": HttpProxy,
    "https": HttpProxy,
}

def get_system_outbounds() -> list[dict]:
    return [
        {
            "tag": "direct",
            "protocol": "freedom",
            "settings": {},
            },
        {
            "tag": "block",
            "protocol": "blackhole",
            "settings": {},
        },
    ]

def get_proxy_class(proxy: Proxy):
    proxy_class = PROTOCOL_REGISTRY.get(proxy.protocol.lower())

    if proxy_class is None:
       raise ValueError(f"Unsupported protocol: {proxy.protocol}")

    return proxy_class

def build_outbound(proxy: Proxy) -> list:
    proxy_class = get_proxy_class(proxy)

    proxy_object = proxy_class(proxy)

    outbound = []

    outbound.extend(proxy_object.get_outbound())
    outbound.extend(get_system_outbounds())

    return outbound