from service.parser import ParsedURL


class VlessProxy:
    known_params = {
        "type", "security", "sni", "fp", "pbk", "sid", "spx", "flow",
        "path", "host", "serviceName", "alpn", "mode"
    }

    def __init__(self, parse_result: ParsedURL):
        self.protocol = parse_result.scheme
        self.uuid = parse_result.username
        self.server = parse_result.hostname
        self.port = parse_result.port
        self.tag = parse_result.fragment

        self.type = parse_result.get_param("type", "tcp")
        self.security = parse_result.get_param("security", "none")
        self.sni = parse_result.get_param("sni")
        self.fp = parse_result.get_param("fp")
        self.pbk = parse_result.get_param("pbk")
        self.sid = parse_result.get_param("sid")
        self.spx = parse_result.get_param("spx")
        self.flow = parse_result.get_param("flow")
        self.path = parse_result.get_param("path", "/")
        self.host = parse_result.get_param("host")
        self.service_name = parse_result.get_param("serviceName")
        self.alpn = parse_result.get_param("alpn")
        self.mode = parse_result.get_param("mode")

        self.extra = parse_result.get_extra_params(self.known_params)

    def get_outbound(self):
        user = {
            "id": self.uuid,
            "encryption": "none",
            "level": 0
        }

        if self.flow:
            user["flow"] = self.flow

        outbound = {
            "tag": self.tag,
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": self.server,
                        "port": self.port,
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

        return [outbound]