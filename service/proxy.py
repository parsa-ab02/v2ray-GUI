from urllib.parse import urlparse, parse_qs, unquote
import service

class Proxy:
    protocol: str
    server: str
    port: int
    username: str
    password: str
    tag: str
    extra_params: list
    structure: dict

    def __init__(self, protocol, server, port, username=None, password=None, tag=None, extra_params=None):
        self.protocol = protocol
        self.server = server
        self.port = port

        self.username = username
        self.password = password
        self.tag = tag

        self.extra_params = extra_params

        self.structure = {
            "log":{
                "loglevel": "warning"
            },
            "inbounds": service.inbounds.get_inbounds(),
            "outbounds": ...,
            "routing": ...
        }

    @classmethod
    def from_URL(cls, URL: str):
        P = urlparse(URL)

        return cls(protocol=P.scheme, server=P.hostname, port=P.port, username=P.username, password=P.password, tag=P.fragment, extra_params=None)

    @classmethod
    def from_file(cls, path:Path):
        with open(path, "r", encoding="utf-8") as file:
            configuration = json.load(file)

        return cls.from_configuration(configuration)

    def from_configuration(cls, configuration: dict):
        ...

        # extract args
        # return cls(*args)

    def get_param(self, key: str, default=None):
        return self.query.get(key, default)

    def get_extra_params(self, known_params: list):
        return{ k: v 
                for k, v in self.query.items()
                if k not in known_params
            }
