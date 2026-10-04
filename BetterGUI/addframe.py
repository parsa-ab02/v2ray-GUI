import customtkinter as ctk
from PIL import Image
from utils import rgb , buttonConfiguration , root
import pyperclip
from service.proxy import Proxy
import json
from service.manager import Manager
from controller import Controller
import requests

icons_directory = root / "icons"

class AddFrame:
    def __init__(self, app:ctk.CTk, controller: Controller):
        self.app = app
        self.controller = controller
        self.AddFrame = ctk.CTkFrame(master=app, width=784 , height=110 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

        self.app.bind_all("<Control-v>", self.import_from_clipboard)
        self.app.bind_all("<Control-V>", self.import_from_clipboard)   

        ImportButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(ImportButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Import.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportClicked.png"), size=(80,80)))
        ImportButton.place(x= 4, y= 4)

        PasteButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10, command=self.import_from_clipboard)
        buttonConfiguration(PasteButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Paste.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteClicked.png"), size=(80,80)))
        PasteButton.place(x= 106, y= 4)

        ManuallyButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(ManuallyButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Manually.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyClicked.png"), size=(80,80)))
        ManuallyButton.place(x= 208, y= 4)


    def show(self):
        self.AddFrame.place(x= 116,y= 306)

    def remove(self):
        self.AddFrame.place_forget()

    def get_clipboard(self) -> str:
        return pyperclip.paste()


    def get_configs_from_sub(self, sub: str) -> str:
        response = requests.get(sub,timeout=10)

        response.raise_for_status()

        data = response.text.strip()
        try:
            return (
                __import__("base64")
                .b64decode(data)
                .decode("utf-8")
            )

        except Exception:
            return data

    def split_entries(self, text: str) -> list[str]:
        entries = []

        buffer = []
        inside_json = False
        depth = 0

        for char in text:
            if char == "{":
                inside_json = True
                depth += 1

            if inside_json:
                buffer.append(char)

                if char == "}":
                    depth -= 1

                    if depth == 0:
                        entries.append("".join(buffer))
                        buffer = []
                        inside_json = False

            else:
                buffer.append(char)
                if char in [",", "\n"]:
                    item = "".join(buffer[:-1]).strip()

                    if item:
                        entries.append(item)

                    buffer = []

        item = "".join(buffer).strip()


        if item:
            entries.append(item)


        return entries

    def looks_like_proxy_url(self, text: str) -> bool:
        return text.startswith(
            (
                "vless://",
                "vmess://",
                "trojan://",
                "hysteria2://",
                "ss://",
                "ssr://",
                "socks://",
                "http://",
                "https://"
            )
        )

    def parse_entry(self, entry: str) -> list:

        proxies = []

        entry = entry.strip()

        if not entry:
            return proxies

        if entry.startswith("{"):
            try:
                config = json.loads(entry)

                proxies.append(Proxy.from_configuration(config))

            except Exception as e:
                print(f"Invalid JSON ignored: {e}")

            return proxies
        if entry.startswith(("http://","https://")):


            try:
                content = self.get_configs_from_sub(entry)

                if ("vless://" in content or "vmess://" in content or
                    "trojan://" in content or"ss://" in content
                    ):

                    urls = self.split_entries(content)

                    for url in urls:
                        try:
                            proxies.append(Proxy.from_URL(url.strip()))

                        except Exception:
                            pass

                else:
                    proxies.append(Proxy.from_URL(entry))

            except Exception as e:
                print(f"Invalid URL ignored: {e}")

            return proxies
        
        if self.looks_like_proxy_url(entry):
            try:
                proxies.append(Proxy.from_URL(entry))

            except Exception as e:
                print(f"Invalid proxy URL ignored: {e}")

        return proxies

    def import_from_clipboard(self, event=None):
        text = self.get_clipboard()

        raw_entries = self.split_entries(text)

        proxies = []

        for entry in raw_entries:
            proxies.extend(self.parse_entry(entry))

        self.add_proxy(proxies)

    def add_proxy(self, proxies: list):
        for proxy in proxies:
            Manager.add(proxy)

            self.controller.configs_frame.create_config_frame(proxy)