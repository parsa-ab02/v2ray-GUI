import customtkinter as ctk
from PIL import Image
from utils import rgb , buttonConfiguration , root

icons_directory = root / "icons"

class AddFrame:
    def __init__(self, app:ctk.CTk):
        self.AddFrame = ctk.CTkFrame(master=app, width=784 , height=110 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

        ImportButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(ImportButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Import.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportClicked.png"), size=(80,80)))
        ImportButton.place(x= 4, y= 4)

        PasteButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(PasteButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Paste.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteClicked.png"), size=(80,80)))
        PasteButton.place(x= 106, y= 4)

        ManuallyButton = ctk.CTkButton(master = self.AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(ManuallyButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Manually.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyClicked.png"), size=(80,80)))
        ManuallyButton.place(x= 208, y= 4)


    def show(self):
        self.AddFrame.place(x= 116,y= 306)

    def remove(self):
        self.AddFrame.place_forget()