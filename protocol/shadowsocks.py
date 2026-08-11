from service.proxy import Proxy


class ShadowsocksProxy:
    known_params = {
        "method","plugin","pluginOpts",
        "type","security", "sni","fp",
        "alpn","path","host","serviceName",
        "mode","pbk", "sid", "spx",
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

        self.method = proxy.get_param("method", "aes-128-gcm")
        self.plugin = proxy.get_param("plugin")
        self.plugin_opts = proxy.get_param("pluginOpts")

        self.type = proxy.get_param("type", "tcp")
        self.security = proxy.get_param("security", "none")

        self.sni = proxy.get_param("sni")
        self.fp = proxy.get_param("fp")
        self.alpn = proxy.get_param("alpn")

        self.path = proxy.get_param("path", "/")
        self.host = proxy.get_param("host")
        self.service_name = proxy.get_param("serviceName")
        self.mode = proxy.get_param("mode")

        self.pbk = proxy.get_param("pbk")
        self.sid = proxy.get_param("sid")
        self.spx = proxy.get_param("spx", "/")

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self):
        outbound = {
            "tag": self.proxy.unquoted_tag,
            "protocol": "shadowsocks",
            "settings": {
                "servers": [{
                    "address": self.proxy.server,
                    "port": self.proxy.port,
                    "method": self.method,
                    "password": self.proxy.username
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