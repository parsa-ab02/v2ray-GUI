from service.proxy import Proxy
from service.protocol_registry import PROTOCOL_REGISTRY

def get_outbound(configuration: dict):
    outbounds = configuration.get("outbounds", [])

    outbound = next(
        (
            outbound
            for outbound in outbounds
            if outbound.get("protocol") not in {"freedom", "blackhole", "dns"}
        ),
        None
    )

    if not outbound:
        raise ValueError("No proxy outbound found")

    return outbound

def get_proxy_class(outbound: dict):
    protocol = outbound.get("protocol")

    proxy_class = PROTOCOL_REGISTRY.get(protocol.lower())

    if proxy_class is None:
        raise ValueError(f"Unsupported protocol: {protocol}")
    
    return proxy_class

def extract_proxy(configuration: dict)-> Proxy:
    outbound = get_outbound(configuration)
    proxy_class = get_proxy_class(outbound)

    proxy_object = proxy_class.extract(outbound)

    if proxy_object is None:
        raise RuntimeError(f"Error: cannot extract proxy, invalid configuration")

    return proxy_object