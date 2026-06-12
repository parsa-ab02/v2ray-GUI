from service.parser import ParsedURL


class Hysteria2Proxy:
    def __init__(self, parsed_url: ParsedURL):
        self.protocol = "hysteria2"
        self.tag = parsed_url.fragment

        self.server = parsed_url.hostname
        self.port = parsed_url.port
        self.password = parsed_url.username

        self.sni = parsed_url.get_param("sni")
        self.alpn = parsed_url.get_param("alpn")

        self.obfs = parsed_url.get_param("obfs")
        self.obfs_password = parsed_url.get_param("obfs-password")

        self.down_mbps = parsed_url.get_param("downmbps")
        self.up_mbps = parsed_url.get_param("upmbps")

        self.insecure = parsed_url.get_param("insecure", "0") == "1"
        self.udp = parsed_url.get_param("udp", "1") == "1"

    def get_outbound(self):
        outbound = {
            "tag": self.tag,
            "protocol": "hysteria2",
            "settings": {
                "server": self.server,
                "server_port": self.port,
                "password": self.password,
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