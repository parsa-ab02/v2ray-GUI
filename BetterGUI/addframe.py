import customtkinter as ctk
from PIL import Image
from utils import rgb , buttonConfiguration , root
import pyperclip
from service.proxy import Proxy
import json
from service.manager import Manager
from controller import Controller

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

    def get_clipboard(self)-> str:
        return pyperclip.paste()

    def split_entries(self, text: str) -> list[Proxy]:

        entries = []

        buffer = []
        inside_json = False
        depth = 0


        def add_url(url):

            url = url.strip()

            if not url:
                return

            try:
                entries.append(
                    Proxy.from_URL(url)
                )

            except Exception:
                print(f"Invalid proxy URL ignored: {url}")


        def add_json(data):

            try:
                configuration = json.loads(data)

                entries.append(
                    Proxy.from_configuration(configuration)
                )

            except Exception as e:
                print(
                    f"Invalid configuration ignored: {e}"
                )


        for char in text:

            if char == "{":

                inside_json = True
                depth += 1


            if inside_json:

                buffer.append(char)

                if char == "}":

                    depth -= 1

                    if depth == 0:

                        add_json(
                            "".join(buffer)
                        )

                        buffer = []
                        inside_json = False


            else:

                buffer.append(char)

                if char in [",", "\n"]:

                    add_url(
                        "".join(buffer[:-1])
                    )

                    buffer = []


        item = "".join(buffer)

        if item:
            add_url(item)


        return entries
    
    def add_proxy(self, proxies: list[Proxy]):
        for proxy in proxies:
            Manager.add(proxy)
            self.controller.configs_frame.create_config_frame(proxy)


    def import_from_clipboard(self, event=None):
        text = self.get_clipboard()
        proxies = self.split_entries(text)
        self.add_proxy(proxies)