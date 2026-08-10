from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path
import json
import service

class Proxy:
    protocol: str
    server: str
    port: int
    username: str | None
    password: str | None
    tag: str | None
    query: dict 
    structure: dict

    def __init__(self, protocol: str, server: str, port: int,
                username: str | None =None,password: str | None =None,
                tag: str | None =None, query: dict | None = None):
        self.protocol = protocol
        self.server = server
        self.port = port

        self.username = username
        self.password = password
        self.tag = tag

        self.query = query or {}

        self.structure = {
            "log":{
                "loglevel": "warning"
            },
            "inbounds": service.inbounds.get_inbounds(),
            "outbounds": [],
            "routing": {}
        }

    @classmethod
    def from_URL(cls, URL: str):
        P = urlparse(URL)

        query = {k: v[0] for k, v in parse_qs(P.query).items()}

        return cls(protocol=P.scheme, server=P.hostname, port=P.port, username=P.username,
                   password=P.password, tag=P.fragment, query=query)

    @classmethod
    def from_file(cls, path: Path):
        with open(path, "r", encoding="utf-8") as file:
            configuration = json.load(file)

        return cls.from_configuration(configuration)

    @classmethod
    def from_configuration(cls, configuration: dict):
        ...

        # extract args
        # return cls(*args)

    def get_param(self, key: str, default=None):
        return self.query.get(key, default)

    def get_extra_params(self, known_params: set[str]) -> dict:
        return{k: v 
                for k, v in self.query.items()
                if k not in known_params
            }

    def to_dict(self):
        return {
            "protocol": self.protocol,
            "server": self.server,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "tag": self.tag,
            "query":self.query
        }

    def __eq__(self, other):
        if not isinstance(other, Proxy):
            return NotImplemented

        return (
            self.protocol == other.protocol and
            self.server == other.server and
            self.port == other.port and
            self.username == other.username and
            self.password == other.password
            # self.query == other.query
        )

    

    def __repr__(self):
        return str(self.to_dict())
