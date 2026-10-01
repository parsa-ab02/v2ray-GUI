import customtkinter as ctk
from pathlib import Path
from PIL import Image
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from service.manager import Manager

from routing import routingFrame
from sidepanel import SidePanel
from mainframe import MainFrame
from addframe import AddFrame
from configsframe import ConfigsFrame
from currentPage import CurrentPage
from controller import Controller

from utils import rgb

root = Path(__file__).resolve().parent
icons_directory = root / "icons"

Manager.read_all()

current_page = CurrentPage.Home
def ShowHome():
    global current_page
    if current_page is CurrentPage.Configs:
        controller.configs_frame.remove_selected_config_info()
    elif current_page is CurrentPage.Routings:
        routings_frame.remove()
    controller.main_frame.show()
    controller.add_frame.show()
    LogsFrame.place(x=116, y= 420)
    current_page = CurrentPage.Home

def ShowConfigs():
    global current_page
    if current_page is CurrentPage.Home:
        controller.main_frame.remove()
        controller.add_frame.remove()
        LogsFrame.place_forget()
    elif current_page is CurrentPage.Routings:
        routings_frame.remove()
    current_page = CurrentPage.Configs
    controller.configs_frame.show_selected_config_info()

def ShowRouting():
    global current_page
    if current_page is CurrentPage.Home:
        controller.main_frame.remove()
        controller.add_frame.remove()
        LogsFrame.place_forget()
    elif current_page is CurrentPage.Configs:
        controller.configs_frame.remove_selected_config_info()
    current_page = CurrentPage.Routings
    routings_frame.show()

def ShowLogs():
    pass

def ShowSettings():
    pass

app = ctk.CTk()
app.title("v2ray GUI")
app.geometry("1500x800")
app.resizable(width=False , height=False)
ctk.set_appearance_mode("dark")

controller = Controller(app)

# -------------- Side Frame ----------------------

controller.side_panel = SidePanel(app, ShowHome, ShowConfigs, ShowRouting)

controller.side_panel.show()

# --------------- Main Frame ----------------------

controller.main_frame = MainFrame(app)

controller.main_frame.show()

#---------------- Add Frame -----------------------

controller.add_frame = AddFrame(app, controller)

controller.add_frame.show()

#---------------- Logs Frame ----------------------

LogsFrame = ctk.CTkFrame(master=app , width=784 , height=378, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
LogsFrame.place(x=116, y= 420)

#---------------- Config Frame --------------------

controller.configs_frame = ConfigsFrame(app)
controller.configs_frame.show()

#---------------- Routing Frame --------------------
routings_frame = routingFrame(app=app)

app.mainloop()