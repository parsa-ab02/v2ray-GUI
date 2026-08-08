import json
import service
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_dir = root / "data"

config_json = data_dir / "config.json"
data_saves = data_dir / "saves.json"

routing_settings = service.routing.get_routing()


class Manager:
    Proxies = []

    @classmethod
    def write(cls, proxy: service.proxy.Proxy, path: Path):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as file:
                json.dump(proxy.structure, file, ensure_ascii=False, indent=4)

        except Exception as e:
            return f"error: {e}"

    @classmethod
    def remove(cls, proxy: service.proxy.Proxy):
        Manager.Proxies = [
            p for p in Manager.Proxies
            if p != proxy
        ]

    @classmethod
    def add(cls, proxy: service.proxy.Proxy):
        Config.config_list.append(proxy)

    @classmethod
    def read_all(cls):
        try:
            with open(data_saves, "r", encoding="utf-8") as file:
                raw_urls = json.load(file)

            cls.Proxies = []

            for raw_url in raw_urls:
                cfg = cls(raw_url)
                cls.config_list.append(cfg)

        except FileNotFoundError:
            cls.config_list = []

        except Exception as e:
            return f"error: {e}"

        return cls.Proxies

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
