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
            "tag": self.proxy.unquoted_tag,
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

    @classmethod
    def extract(cls, outbound: dict) -> Proxy:
        settings = outbound.get("settings", {})
        server = settings.get("servers", [{}])[0]

        stream = outbound.get("streamSettings", {})

        params = {}

        password = server.get("password")

        network = stream.get("network")

        if network:
            params["type"] = network

        security = stream.get("security")

        if security:
            params["security"] = security

        if security == "tls":
            tls = stream.get("tlsSettings", {})

            if tls.get("serverName"):
                params["sni"] = tls["serverName"]

            if tls.get("fingerprint"):
                params["fp"] = tls["fingerprint"]

            if tls.get("alpn"):
                params["alpn"] = ",".join(tls["alpn"])

        elif security == "reality":
            reality = stream.get("realitySettings", {})

            if reality.get("serverName"):
                params["sni"] = reality["serverName"]

            if reality.get("publicKey"):
                params["pbk"] = reality["publicKey"]

            if reality.get("shortId"):
                params["sid"] = reality["shortId"]

            if reality.get("fingerprint"):
                params["fp"] = reality["fingerprint"]

            if reality.get("spiderX"):
                params["spx"] = reality["spiderX"]

        if network == "ws":
            ws = stream.get("wsSettings", {})

            if ws.get("path"):
                params["path"] = ws["path"]

            headers = ws.get("headers", {})

            if headers.get("Host"):
                params["host"] = headers["Host"]

        elif network == "grpc":
            grpc = stream.get("grpcSettings", {})

            if grpc.get("serviceName"):
                params["serviceName"] = grpc["serviceName"]

            if grpc.get("multiMode"):
                params["mode"] = "multi"

        elif network == "http":
            http = stream.get("httpSettings", {})

            if http.get("path"):
                params["path"] = http["path"]

            hosts = http.get("host", [])

            if hosts:
                params["host"] = hosts[0]

        return Proxy(
            protocol="trojan",
            server=server.get("address"),
            port=int(server.get("port")),
            username=password,
            tag=outbound.get("tag"),
            extra_params=params
        )