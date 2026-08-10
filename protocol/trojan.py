from service.proxy import Proxy


class TrojanProxy:
    known_params = {
        "type", "security", "sni", "fp", "alpn",
        "pbk", "sid", "spx",
        "path", "host", "serviceName", "mode"
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

        self.type = proxy.get_param("type", "tcp")

        self.security = proxy.get_param("security", "tls")
        self.sni = proxy.get_param("sni")
        self.fp = proxy.get_param("fp")
        self.alpn = proxy.get_param("alpn")

        self.pbk = proxy.get_param("pbk")
        self.sid = proxy.get_param("sid")
        self.spx = proxy.get_param("spx", "/")

        self.path = proxy.get_param("path", "/")
        self.host = proxy.get_param("host")
        self.service_name = proxy.get_param("serviceName")
        self.mode = proxy.get_param("mode")

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self):
        outbound = {
            "tag": self.proxy.tag,
            "protocol": "trojan",
            "settings": {
                "servers": [{
                    "address": self.proxy.server,
                    "port": self.proxy.port,
                    "password": self.proxy.username,
                    "level": 0
                }]
            },
            "streamSettings": {
                "network": self.type,
            }
        }

        if self.security == "tls":
            outbound["streamSettings"]["security"] = "tls"

            tls_settings = {
                "serverName": self.sni,
                "fingerprint": self.fp,
            }

            if self.alpn:
                tls_settings["alpn"] = [self.alpn]

            outbound["streamSettings"]["tlsSettings"] = {
                k: v for k, v in tls_settings.items() if v
            }

        elif self.security == "reality":
            outbound["streamSettings"]["security"] = "reality"

            reality_settings = {
                "serverName": self.sni,
                "publicKey": self.pbk,
                "shortId": self.sid,
                "fingerprint": self.fp,
                "spiderX": self.spx or self.path
            }

            outbound["streamSettings"]["realitySettings"] = {
                k: v for k, v in reality_settings.items() if v
            }

        else:
            outbound["streamSettings"]["security"] = "none"

        if self.type == "ws":
            ws = {"path": self.path}
            if self.host:
                ws["headers"] = {"Host": self.host}

            outbound["streamSettings"]["wsSettings"] = ws

        if self.type == "grpc":
            outbound["streamSettings"]["grpcSettings"] = {
                "serviceName": self.service_name or "",
                "multiMode": self.mode == "multi"
            }

        if self.type == "http":
            outbound["streamSettings"]["httpSettings"] = {
                "path": self.path,
                "host": [self.host] if self.host else []
            }

        outbound["streamSettings"] = {
            k: v for k, v in outbound["streamSettings"].items()
            if v not in [None, {}, []]
        }

        return [outbound]