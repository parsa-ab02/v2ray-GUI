from service.proxy import Proxy


class VmessProxy:
    known_params = {
        "alterId", "security", "type", "tls", "sni", "fp", "alpn",
        "path", "host", "serviceName", "mode", "quicSecurity", "key", "headerType"
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

        self.alter_id = int(proxy.get_param("alterId", "0"))
        self.user_security = proxy.get_param("security", "auto")
        self.type = proxy.get_param("type", "tcp")
        self.tls = proxy.get_param("tls", "none")
        self.sni = proxy.get_param("sni")
        self.fp = proxy.get_param("fp")
        self.alpn = proxy.get_param("alpn")
        self.path = proxy.get_param("path", "/")
        self.host = proxy.get_param("host")
        self.service_name = proxy.get_param("serviceName")
        self.mode = proxy.get_param("mode")
        self.quic_security = proxy.get_param("quicSecurity", "none")
        self.quic_key = proxy.get_param("key", "")
        self.quic_header = proxy.get_param("headerType", "none")

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self):
        outbound = {
            "tag": self.proxy.unquoted_tag,
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": self.proxy.server,
                        "port": self.proxy.port,
                        "users": [
                            {
                                "id": self.proxy.username,
                                "alterId": self.alter_id,
                                "security": self.user_security,
                                "level": 0
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": self.type,
                "security": "none"
            }
        }

        if self.tls in ["tls", "true"]:
            outbound["streamSettings"]["security"] = "tls"

            tls_settings = {}

            if self.sni:
                tls_settings["serverName"] = self.sni

            if self.fp:
                tls_settings["fingerprint"] = self.fp

            if self.alpn:
                tls_settings["alpn"] = [self.alpn]

            outbound["streamSettings"]["tlsSettings"] = tls_settings

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
                "security": self.quic_security,
                "key": self.quic_key,
                "header": {
                    "type": self.quic_header
                }
            }

        return [outbound]