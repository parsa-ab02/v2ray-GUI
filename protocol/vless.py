from service.proxy import Proxy


class VlessProxy:
    known_params = {
        "type", "security", "sni", "fp", "pbk", "sid", "spx", "flow",
        "path", "host", "serviceName", "alpn", "mode"
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy 

        self.type = proxy.get_param("type", "tcp")
        self.security = proxy.get_param("security", "none")
        self.sni = proxy.get_param("sni")
        self.fp = proxy.get_param("fp")
        self.pbk = proxy.get_param("pbk")
        self.sid = proxy.get_param("sid")
        self.spx = proxy.get_param("spx")
        self.flow = proxy.get_param("flow")
        self.path = proxy.get_param("path", "/")
        self.host = proxy.get_param("host")
        self.service_name = proxy.get_param("serviceName")
        self.alpn = proxy.get_param("alpn")
        self.mode = proxy.get_param("mode")

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self) -> list[dict]:
        user = {
            "id": self.proxy.username,
            "encryption": "none",
            "level": 0
        }

        if self.flow:
            user["flow"] = self.flow

        outbound = {
            "tag": self.proxy.unquoted_tag,
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": self.proxy.server,
                        "port": self.proxy.port,
                        "users": [user]
                    }
                ]
            },
            "streamSettings": {
                "network": self.type,
                "security": self.security
            }
        }

        if self.security == "tls":
            tls_settings = {}

            if self.sni:
                tls_settings["serverName"] = self.sni

            if self.fp:
                tls_settings["fingerprint"] = self.fp

            if self.alpn:
                tls_settings["alpn"] = [self.alpn]

            outbound["streamSettings"]["tlsSettings"] = tls_settings

        if self.security == "reality":
            outbound["streamSettings"]["realitySettings"] = {
                "serverName": self.sni,
                "publicKey": self.pbk,
                "shortId": self.sid,
                "fingerprint": self.fp,
                "spiderX": self.spx or self.path or "/"
            }

        if self.type == "ws":
            ws_settings = {
                "path": self.path or "/"
            }

            if self.host:
                ws_settings["headers"] = {
                    "Host": self.host
                }

            outbound["streamSettings"]["wsSettings"] = ws_settings

        if self.type == "grpc":
            outbound["streamSettings"]["grpcSettings"] = {
                "serviceName": self.service_name or "",
                "multiMode": self.mode == "multi"
            }

        if self.type == "http":
            outbound["streamSettings"]["httpSettings"] = {
                "path": self.path or "/",
                "host": [self.host] if self.host else []
            }

        if self.type == "quic":
            outbound["streamSettings"]["quicSettings"] = {
                "security": "none",
                "key": "",
                "header": {
                    "type": "none"
                }
            }
        if self.type == "httpupgrade":
            httpupgrade_settings = {
                "path": self.path or "/"
            }

            if self.host:
                httpupgrade_settings["host"] = self.host

            outbound["streamSettings"]["httpupgradeSettings"] = httpupgrade_settings

        return [outbound]

    @classmethod
    def extract(cls, outbound: dict) -> Proxy:
        settings = outbound.get("settings", {})
        vnext = settings.get("vnext", [{}])[0]

        user = vnext.get("users", [{}])[0]

        stream = outbound.get("streamSettings", {})

        params = {}

        if user.get("flow"):
            params["flow"] = user["flow"]

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


        elif network == "quic":
            quic = stream.get("quicSettings", {})

            params["security"] = quic.get(
                "security",
                "none"
            )

        elif network == "httpupgrade":
            httpupgrade = stream.get(
                "httpupgradeSettings",
                {}
            )

            if httpupgrade.get("path"):
                params["path"] = httpupgrade["path"]

            if httpupgrade.get("host"):
                params["host"] = httpupgrade["host"]


        return Proxy(
            protocol="vless",
            server=vnext.get("address"),
            port=int(vnext.get("port")),
            username=user.get("id"),
            tag=outbound.get("tag"),
            extra_params=params
        )