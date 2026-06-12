from service.parser import ParsedURL


class TrojanProxy:
    def __init__(self, parsed_url: ParsedURL):
        self.protocol = "trojan"
        self.tag = parsed_url.fragment

        self.password = parsed_url.username
        self.server = parsed_url.hostname
        self.port = parsed_url.port

        self.type = parsed_url.get_param("type", "tcp")

        self.security = parsed_url.get_param("security", "tls")
        self.sni = parsed_url.get_param("sni")
        self.fp = parsed_url.get_param("fp")
        self.alpn = parsed_url.get_param("alpn")

        self.pbk = parsed_url.get_param("pbk")
        self.sid = parsed_url.get_param("sid")
        self.spx = parsed_url.get_param("spx", "/")

        self.path = parsed_url.get_param("path", "/")
        self.host = parsed_url.get_param("host")
        self.service_name = parsed_url.get_param("serviceName")
        self.mode = parsed_url.get_param("mode")

    def get_outbound(self):
        outbound = {
            "tag": self.tag,
            "protocol": "trojan",
            "settings": {
                "servers": [{
                    "address": self.server,
                    "port": self.port,
                    "password": self.password,
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