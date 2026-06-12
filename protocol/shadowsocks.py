from service.parser import ParsedURL


class ShadowsocksProxy:
    def __init__(self, parsed_url: ParsedURL):
        self.protocol = "shadowsocks"
        self.tag = parsed_url.fragment

        self.password = parsed_url.username
        self.server = parsed_url.hostname
        self.port = parsed_url.port

        self.method = parsed_url.get_param("method", "aes-128-gcm")
        self.plugin = parsed_url.get_param("plugin")
        self.plugin_opts = parsed_url.get_param("pluginOpts")

        self.type = parsed_url.get_param("type", "tcp")
        self.security = parsed_url.get_param("security", "none")

        self.sni = parsed_url.get_param("sni")
        self.fp = parsed_url.get_param("fp")
        self.alpn = parsed_url.get_param("alpn")

        self.path = parsed_url.get_param("path", "/")
        self.host = parsed_url.get_param("host")
        self.service_name = parsed_url.get_param("serviceName")
        self.mode = parsed_url.get_param("mode")

        self.pbk = parsed_url.get_param("pbk")
        self.sid = parsed_url.get_param("sid")
        self.spx = parsed_url.get_param("spx", "/")

    def get_outbound(self):
        outbound = {
            "tag": self.tag,
            "protocol": "shadowsocks",
            "settings": {
                "servers": [{
                    "address": self.server,
                    "port": self.port,
                    "method": self.method,
                    "password": self.password
                }]
            },
            "streamSettings": {
                "network": self.type
            }
        }

        if self.plugin:
            outbound["settings"]["servers"][0]["plugin"] = self.plugin
            if self.plugin_opts:
                outbound["settings"]["servers"][0]["pluginOpts"] = self.plugin_opts

        if self.security == "tls":
            outbound["streamSettings"]["security"] = "tls"

            tls = {
                "serverName": self.sni,
                "fingerprint": self.fp
            }

            if self.alpn:
                tls["alpn"] = [self.alpn]

            outbound["streamSettings"]["tlsSettings"] = {
                k: v for k, v in tls.items() if v
            }

        elif self.security == "reality":
            outbound["streamSettings"]["security"] = "reality"

            reality = {
                "serverName": self.sni,
                "publicKey": self.pbk,
                "shortId": self.sid,
                "fingerprint": self.fp,
                "spiderX": self.spx or self.path
            }

            outbound["streamSettings"]["realitySettings"] = {
                k: v for k, v in reality.items() if v
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

        if self.type == "quic":
            outbound["streamSettings"]["quicSettings"] = {
                "security": "none",
                "key": "",
                "header": {"type": "none"}
            }

        outbound["streamSettings"] = {
            k: v for k, v in outbound["streamSettings"].items()
            if v not in [None, {}, []]
        }

        return [outbound]