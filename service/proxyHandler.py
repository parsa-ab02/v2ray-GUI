from service.proxy import Proxy
from service.protocol_registry import PROTOCOL_REGISTRY

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