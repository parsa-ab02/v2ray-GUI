from service.parser import ParsedURL


class HttpProxy:
    def __init__(self, parsed_url: ParsedURL):
        self.protocol = "http"
        self.tag = parsed_url.fragment

        self.server = parsed_url.hostname
        self.port = parsed_url.port

        self.username = parsed_url.username
        self.password = parsed_url.password

        self.security = parsed_url.get_param("security", "none")
        self.sni = parsed_url.get_param("sni")
        self.alpn = parsed_url.get_param("alpn")
        self.fp = parsed_url.get_param("fp")

        self.insecure = parsed_url.get_param("insecure", "0") == "1"

    def get_outbound(self):

        server = {
            "address": self.server,
            "port": self.port
        }

        if self.username:
            server["users"] = [{
                "user": self.username,
                "pass": self.password or ""
            }]

        outbound = {
            "tag": self.tag,
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