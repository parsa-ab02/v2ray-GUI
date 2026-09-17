import customtkinter as ctk
from utils import rgb, ConnectButtonConfiguration, root
from PIL import Image

icons_directory = root / "icons"

class MainFrame:
    def __init__(self, app:ctk.CTk):
        self.MainFrame = ctk.CTkFrame(master=app, width=784 , height=300 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
        self.ConnectButton = ctk.CTkButton(master=self.MainFrame , width= 200, height=200 , text= "" , fg_color=rgb((19, 19, 54)))

        ConnectButtonConfiguration(
            self.ConnectButton,
            Image.open(icons_directory / "Connect.png"),
            Image.open(icons_directory / "ConnectHover.png"),
            Image.open(icons_directory / "ConnectClicked.png"),
            Image.open(icons_directory / "Connected.png"),
            Image.open(icons_directory / "ConnectedHover.png"),
            Image.open(icons_directory / "ConnectedClicked.png")
        )
        self.ConnectButton.place(x= 10 , y= 50)

        self.StatusLabel = ctk.CTkLabel(master=self.MainFrame, text="Status : Not Connected" , font=ctk.CTkFont(family="Fredoka", size=30))
        self.DownLinkLabel = ctk.CTkLabel(master=self.MainFrame, text="DownLink" , font=ctk.CTkFont(family="Fredoka", size=30))
        self.UpLinkLabel = ctk.CTkLabel(master=self.MainFrame, text="UpLink" , font=ctk.CTkFont(family="Fredoka", size=30))

        self.StatusLabel.place(x=280,y=50)
        self.DownLinkLabel.place(x=280,y=100)
        self.UpLinkLabel.place(x=450,y=100)

    def show(self):
        self.MainFrame.place(x=116 , y= 2)

    def remove(self):
        self.MainFrame.place_forget()
