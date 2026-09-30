from service.proxy import Proxy


class HttpProxy:
    known_params = {
        "security","sni","alpn","fp", "insecure",
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

        self.security = proxy.get_param("security", "none")
        self.sni = proxy.get_param("sni")
        self.alpn = proxy.get_param("alpn")
        self.fp = proxy.get_param("fp")

        self.insecure = proxy.get_param("insecure", "0") == "1"

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self):

        server = {
            "address": self.proxy.server,
            "port": self.proxy.port
        }

        if self.proxy.username:
            server["users"] = [{
                "user": self.proxy.username,
                "pass": self.proxy.password or ""
            }]

        outbound = {
            "tag": self.proxy.unquoted_tag,
            "protocol": "http",
            "settings": {
                "servers": [server]
            }
        }

        if self.security == "tls":
            outbound["streamSettings"] = {
                "security": "tls",
                "tlsSettings": {
                    "serverName": self.sni,
                    "fingerprint": self.fp,
                    "allowInsecure": self.insecure
                }
            }

            if self.alpn:
                outbound["streamSettings"]["tlsSettings"]["alpn"] = [self.alpn]

        return [outbound]

    @classmethod
    def extract(cls, outbound: dict) -> Proxy:
        settings = outbound.get("settings", {})

        server = settings.get("servers", [{}])[0]

        params = {}

        stream = outbound.get("streamSettings", {})

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

            if tls.get("allowInsecure"):
                params["insecure"] = "1"

        users = server.get("users", [])

        username = None
        password = None

        if users:
            user = users[0]

            username = user.get("user")
            password = user.get("pass")

        return Proxy(
            protocol="http",
            server=server.get("address"),
            port=int(server.get("port")),
            username=username,
            password=password,
            tag=outbound.get("tag"),
            extra_params=params
        )