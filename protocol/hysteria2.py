from service.proxy import Proxy


class Hysteria2Proxy:
    known_params = {
        "sni","alpn", "obfs","obfs-password",
        "downmbps","upmbps","insecure", "udp",
    }

    def __init__(self, proxy: Proxy):
        self.proxy = proxy

        self.sni = proxy.get_param("sni")
        self.alpn = proxy.get_param("alpn")

        self.obfs = proxy.get_param("obfs")
        self.obfs_password = proxy.get_param("obfs-password")

        self.down_mbps = proxy.get_param("downmbps")
        self.up_mbps = proxy.get_param("upmbps")

        self.insecure = proxy.get_param("insecure", "0") == "1"
        self.udp = proxy.get_param("udp", "1") == "1"

        self.extra = proxy.get_extra_params(self.known_params)

    def get_outbound(self):
        outbound = {
            "tag": self.proxy.unquoted_tag,
            "protocol": "hysteria2",
            "settings": {
                "server": self.proxy.server,
                "server_port": self.proxy.port,
                "password": self.proxy.username,
            },
            "streamSettings": {
                "network": "tcp"
            }
        }

        tls = {
            "serverName": self.sni,
            "allowInsecure": self.insecure
        }

        if self.alpn:
            tls["alpn"] = [self.alpn]

        outbound["streamSettings"]["tlsSettings"] = {
            k: v for k, v in tls.items() if v not in [None, []]
        }

        if self.obfs:
            outbound["settings"]["obfs"] = {
                "type": self.obfs,
                "password": self.obfs_password or ""
            }

        if self.up_mbps or self.down_mbps:
            bw = {}
            if self.up_mbps:
                bw["up"] = self.up_mbps + " mbps"
            if self.down_mbps:
                bw["down"] = self.down_mbps + " mbps"

            outbound["settings"]["bandwidth"] = bw

        outbound["settings"] = {k: v for k, v in outbound["settings"].items() if v}
        outbound["streamSettings"] = {k: v for k, v in outbound["streamSettings"].items() if v}

        return [outbound]