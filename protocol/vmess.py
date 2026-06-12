from service.parser import ParsedURL


class VmessProxy:
    known_params = {
        "alterId", "security", "type", "tls", "sni", "fp", "alpn",
        "path", "host", "serviceName", "mode", "quicSecurity", "key", "headerType"
    }

    def __init__(self, parse_result: ParsedURL):
        self.protocol = "vmess"
        self.tag = parse_result.fragment
        self.uuid = parse_result.username
        self.server = parse_result.hostname
        self.port = parse_result.port

        self.alter_id = int(parse_result.get_param("alterId", "0"))
        self.user_security = parse_result.get_param("security", "auto")
        self.type = parse_result.get_param("type", "tcp")
        self.tls = parse_result.get_param("tls", "none")
        self.sni = parse_result.get_param("sni")
        self.fp = parse_result.get_param("fp")
        self.alpn = parse_result.get_param("alpn")
        self.path = parse_result.get_param("path", "/")
        self.host = parse_result.get_param("host")
        self.service_name = parse_result.get_param("serviceName")
        self.mode = parse_result.get_param("mode")
        self.quic_security = parse_result.get_param("quicSecurity", "none")
        self.quic_key = parse_result.get_param("key", "")
        self.quic_header = parse_result.get_param("headerType", "none")

        self.extra = parse_result.get_extra_params(self.known_params)

    def get_outbound(self):
        outbound = {
            "tag": self.tag,
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": self.server,
                        "port": self.port,
                        "users": [
                            {
                                "id": self.uuid,
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