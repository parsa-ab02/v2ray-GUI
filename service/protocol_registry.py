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