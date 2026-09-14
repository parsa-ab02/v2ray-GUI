import customtkinter as ctk
from PIL import Image
from utils import rgb , buttonConfiguration , root

icons_directory = root / "icons"

class SidePanel:
    def __init__(self, app: ctk.CTk, ShowHome, ShowConfigs, ShowRouting):
        self.SideFrame = ctk.CTkFrame(master=app , width=110 , height=796 , fg_color=rgb((19, 19, 54)) ,border_width=2 , border_color="white")

        HomeButton = ctk.CTkButton(master = self.SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(HomeButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Home.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "HomeHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "HomeClicked.png"), size=(80,80)) , command=ShowHome)
        HomeButton.place(x=4,y=4)

        ConfigsButton = ctk.CTkButton(master = self.SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(ConfigsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Configs.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ConfigsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ConfigsClicked.png"), size=(80,80)) , command=ShowConfigs)
        ConfigsButton.place(x=4 , y=106)

        RoutingButton = ctk.CTkButton(master = self.SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(RoutingButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Routing.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "RoutingHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "RoutingClicked.png"), size=(80,80)), command=ShowRouting)
        RoutingButton.place(x=4 , y= 208)

        LogsButton = ctk.CTkButton(master = self.SideFrame ,width=100 ,text= "",fg_color=rgb((24, 0, 173)) , hover_color=rgb((24, 0, 173)),  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(LogsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Logs.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "LogsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "LogsClicked.png"), size=(80,80)))
        LogsButton.place(x=4 , y= 310)

        SettingsButton = ctk.CTkButton(master = self.SideFrame ,width=100 ,text= "",fg_color=rgb((24, 0, 173)) , hover_color=rgb((24, 0, 173)),  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(SettingsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Settings.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "SettingsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "SettingsClicked.png"), size=(80,80)))
        SettingsButton.place(x=4 , y = 692)

    def show(self):
        self.SideFrame.place(x = 2 , y = 2)

    def remove(self):
        self.SideFrame.place_forget()