from urllib.parse import urlparse, parse_qs, unquote
import service
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
class Proxy:
    protocol: str
    server: str
    port: int
    username: str
    password: str
    tag: str
    extra_params: list
    query: dict
    structure: dict

    def __init__(self, protocol, server, port, username=None, password=None, tag=None, extra_params=None):
        self.protocol = protocol
        self.server = server
        self.port = port

        self.username = username
        self.password = password
        self.tag = tag

        self.query = extra_params

        self.structure = {
            "log":{
                "loglevel": "warning"
            },
            "inbounds": service.inbounds.get_inbounds(),
            "outbounds": build_outbound()
            "routing": {}
        }

    @classmethod
    def get_system_outbounds() -> list[dict]:
        return [
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {},

            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {},
            },
        ]

    @classmethod
    def from_URL(cls, URL: str) -> cls:
        P = urlparse(URL)

        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        return cls(protocol=P.scheme, server=P.hostname, port=P.port, username=P.username,
                   password=P.password, tag=P.fragment, extra_params=query)

    @classmethod
    def from_file(cls, path:Path) -> cls:
        with open(path, "r", encoding="utf-8") as file:
            configuration = json.load(file)

        return cls.from_configuration(configuration)

    def from_configuration(cls, configuration: dict) -> cls:
        ...

        # extract args
        # return cls(*args)

    def get_param(self, key: str, default=None) -> str:
        return self.query.get(key, default)

    def get_extra_params(self, known_params: list) -> dict:
        return{ k: v 
                for k, v in self.query.items()
                if k not in known_params
            }

    def get_proxy_class(self):
        proxy_class = PROTOCOL_REGISTRY.get(self.protocol.lower())

        if proxy_class is None:
            raise ValueError(f"Unsupported protocol: {scheme}")

        return proxy_class

    def build_outbound(self) -> list:
        proxy_class = get_proxy_class(p.protocol)

        proxy = proxy_class(self)

        outbound = []

        outbound.extend(proxy.get_outbound())
        outbound.extend(get_system_outbounds())

        return outbound
