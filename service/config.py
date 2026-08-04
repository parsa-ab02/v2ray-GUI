import json
import service
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_dir = root / "data"

config_json = data_dir / "config.json"
data_saves = data_dir / "saves.json"

routing_settings = service.routing.get_routing()


class Config:
    config_list = []

    def __init__(self, raw_url: str):
        self.raw_url = raw_url
        self.ParsedUrl = service.url_handler.parse(self.raw_url)
        self.tag = self.ParsedUrl.fragment
        self.protocol = self.ParsedUrl.scheme
        self.port = self.ParsedUrl.port

        self.structure = {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": service.inbounds.get_inbounds(),
            "outbounds": service.url_handler.build_outbound(self.raw_url),
            "routing": routing_settings
        }
    
    @classmethod
    def from_url(cls, raw_url: str):
        ...

    @classmethod
    def from_kwargs(cls, *args, **kwargs):
        ...

    @classmethod
    def from_configuration(cls, configuration: str):
        ...

    def write(self):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)

            with open(config_json, "w", encoding="utf-8") as file:
                json.dump(self.structure, file, ensure_ascii=False, indent=4)

        except Exception as e:
            return f"error: {e}"
    
    def remove(self):
        Config.config_list = [
            cfg for cfg in Config.config_list
            if cfg.raw_url != self.raw_url
        ]

    def add(self):
        Config.config_list.append(self)

    @classmethod
    def read_all(cls):
        try:
            with open(data_saves, "r", encoding="utf-8") as file:
                raw_urls = json.load(file)

            cls.config_list = []

            for raw_url in raw_urls:
                cfg = cls(raw_url)
                cls.config_list.append(cfg)

        except FileNotFoundError:
            cls.config_list = []

        except Exception as e:
            return f"error: {e}"

        return cls.config_list

    @classmethod
    def save(cls):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)

            raw_urls = []

            for cfg in cls.config_list:
                raw_urls.append(cfg.raw_url)

            with open(data_saves, "w", encoding="utf-8") as file:
                json.dump(raw_urls, file, ensure_ascii=False, indent=4)

        except Exception as e:
            return f"error: {e}"
