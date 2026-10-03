import json
from service import proxy
from pathlib import Path
from service import routing

root = Path(__file__).resolve().parent.parent
data_dir = root / "data"

config_json = data_dir / "config.json"
data_saves = data_dir / "saves.json"
routing_saves = data_dir / "routing.json"


class Manager:
    Proxies = []

    @classmethod
    def write(cls, proxy: proxy.Proxy, path: Path = config_json):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as file:
                json.dump(proxy.get_structure(), file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"error: {e}")
            return f"error: {e}"

    @classmethod
    def remove(cls, proxy: proxy.Proxy):
        cls.Proxies = [
            p for p in Manager.Proxies
            if p != proxy
        ]

    @classmethod
    def add(cls, proxy: proxy.Proxy):
        cls.Proxies.append(proxy)

    @classmethod
    def read_all(cls):
        try:
            with open(data_saves, "r", encoding="utf-8") as file:
                proxies_kwargs = json.load(file)

            cls.Proxies = []

            for kwargs in proxies_kwargs:
                prxy = proxy.Proxy(**kwargs)
                cls.Proxies.append(prxy)

        except FileNotFoundError:
            cls.Proxies = []

        except Exception as e:
            return f"error: {e}"

    @classmethod
    def read_routings(cls):
        try:
            with open(routing_saves, "r", encoding="utf-8") as file:
                routing.ROUTING_PROFILES = json.load(file)
        except FileNotFoundError:
            routing.ROUTING_PROFILES = {
                "full_tunnel": {
                "domainStrategy": "AsIs",
                "rules": []
                },
            }
        except Exception as e:
            return f"error: {e}"
        finally:
            routing.Routing_profile = routing.get_routing("full_tunnel")

    @classmethod
    def save(cls):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)

            listof_proxies_dicts = [proxy.to_dict() for proxy in cls.Proxies]

            with open(data_saves, "w", encoding="utf-8") as file:
                json.dump(listof_proxies_dicts, file, ensure_ascii=False, indent=4)

            with open(routing_saves, "w", encoding="utf-8") as file:
                json.dump(cls.Routings, file, ensure_ascii=False, indent=4)

        except Exception as e:
            return f"error: {e}"
