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

    def get_outbound(self) -> dict:
        user = {
            "id": self.proxy.username,
            "encryption": "none",
            "level": 0
        }

        if self.flow:
            user["flow"] = self.flow

        outbound = {
            "tag": self.proxy.tag,
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



        return outbound

from service.proxy import Proxy


class VlessProxy:
    known_params = {
        "type", "security", "sni", "fp", "pbk", "sid", "spx", "flow",
        "path", "host", "serviceName", "alpn", "mode"
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    def get_outbound(self):
        proxy = self.proxy

        network = proxy.get_param("type", "tcp")
        security = proxy.get_param("security", "none")
        flow = proxy.get_param("flow")

        user = {
            "id": proxy.username,
            "encryption": "none",
            "level": 0
        }

        if flow:
            user["flow"] = flow

        outbound = {
            "tag": proxy.tag,
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": proxy.server,
                        "port": proxy.port,
                        "users": [user]
                    }
                ]
            },
            "streamSettings": {
                "network": network,
                "security": security
            }
        }

        if security == "tls":
            tls_settings = {}

            sni = proxy.get_param("sni")
            fp = proxy.get_param("fp")
            alpn = proxy.get_param("alpn")

            if sni:
                tls_settings["serverName"] = sni

            if fp:
                tls_settings["fingerprint"] = fp

            if alpn:
                tls_settings["alpn"] = [alpn]

            outbound["streamSettings"]["tlsSettings"] = tls_settings

        elif security == "reality":
            sni = proxy.get_param("sni")
            pbk = proxy.get_param("pbk")
            sid = proxy.get_param("sid")
            fp = proxy.get_param("fp")
            spx = proxy.get_param("spx")
            path = proxy.get_param("path", "/")

            outbound["streamSettings"]["realitySettings"] = {
                "serverName": sni,
                "publicKey": pbk,
                "shortId": sid,
                "fingerprint": fp,
                "spiderX": spx or path or "/"
            }

        if network == "ws":
            path = proxy.get_param("path", "/")
            host = proxy.get_param("host")

            ws_settings = {
                "path": path or "/"
            }

            if host:
                ws_settings["headers"] = {
                    "Host": host
                }

            outbound["streamSettings"]["wsSettings"] = ws_settings

        elif network == "grpc":
            service_name = proxy.get_param("serviceName")
            mode = proxy.get_param("mode")

            outbound["streamSettings"]["grpcSettings"] = {
                "serviceName": service_name or "",
                "multiMode": mode == "multi"
            }

        elif network == "http":
            path = proxy.get_param("path", "/")
            host = proxy.get_param("host")

            outbound["streamSettings"]["httpSettings"] = {
                "path": path or "/",
                "host": [host] if host else []
            }

        elif network == "quic":
            outbound["streamSettings"]["quicSettings"] = {
                "security": "none",
                "key": "",
                "header": {
                    "type": "none"
                }
            }

        elif network == "httpupgrade":
            path = proxy.get_param("path", "/")
            host = proxy.get_param("host")

            httpupgrade_settings = {
                "path": path or "/"
            }

            if host:
                httpupgrade_settings["host"] = host

            outbound["streamSettings"]["httpupgradeSettings"] = (
                httpupgrade_settings
            )

        return [outbound]
