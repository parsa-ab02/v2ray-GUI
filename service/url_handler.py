from service.parser import ParsedURL

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

def parse(raw_url: str) -> ParsedURL:
    return ParsedURL(raw_url)

def get_proxy_class(scheme: str):
    scheme = scheme.lower()

    proxy_class = PROTOCOL_REGISTRY.get(scheme)

    if proxy_class is None:
        raise ValueError(f"Unsupported protocol: {scheme}")

    return proxy_class

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

def build_outbound(raw_url: str) -> list:
    parsed_url = parse(raw_url)

    proxy_class = get_proxy_class(parsed_url.scheme)

    proxy = proxy_class(parsed_url)

    outbound = []

    outbound.extend(proxy.get_outbound())
    outbound.extend(get_system_outbounds())

    return outbound