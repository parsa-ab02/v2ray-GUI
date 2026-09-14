import customtkinter as ctk
from utils import rgb
from pathlib import Path
from PIL import Image
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from service.manager import Manager
from service.proxy import Proxy

from routing import routingFrame
from sidepanel import SidePanel
from mainframe import MainFrame

from utils import buttonConfiguration

root = Path(__file__).resolve().parent
icons_directory = root / "icons"

Manager.read_all()

current_page = "Home"
def ShowHome():
    global current_page
    if current_page == "Configs":
        SelectedConfigInfo.place_forget()
    elif current_page == "Routings":
        routings_frame.remove()
    main_frame.show()
    AddFrame.place(x= 116,y= 306)
    LogsFrame.place(x=116, y= 420)
    current_page = "Home"

def ShowConfigs():
    global current_page
    if current_page == "Home":
        main_frame.remove()
        AddFrame.place_forget()
        LogsFrame.place_forget()
    elif current_page == "Routings":
        routings_frame.remove()
    current_page = "Configs"
    createSelectedConfigInfo()

def ShowRouting():
    global current_page
    if current_page == "Home":
        main_frame.remove()
        AddFrame.place_forget()
        LogsFrame.place_forget()
    elif current_page == "Configs":
        SelectedConfigInfo.place_forget()
    current_page = "Routings"
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

# -------------- Side Frame ----------------------

SideFrme = SidePanel(app, ShowHome, ShowConfigs, ShowRouting)
SideFrme.show()

# --------------- Main Frame ----------------------

main_frame = MainFrame(app)

main_frame.show()

#---------------- Add Frame -----------------------

AddFrame = ctk.CTkFrame(master=app, width=784 , height=110 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

ImportButton = ctk.CTkButton(master = AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(ImportButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Import.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ImportClicked.png"), size=(80,80)))
ImportButton.place(x= 4, y= 4)

PasteButton = ctk.CTkButton(master = AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(PasteButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Paste.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "PasteClicked.png"), size=(80,80)))
PasteButton.place(x= 106, y= 4)

ManuallyButton = ctk.CTkButton(master = AddFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(ManuallyButton ,ctk.CTkImage(dark_image=Image.open(icons_directory / "Manually.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ManuallyClicked.png"), size=(80,80)))
ManuallyButton.place(x= 208, y= 4)


AddFrame.place(x= 116,y= 306)
#---------------- Logs Frame ----------------------

LogsFrame = ctk.CTkFrame(master=app , width=784 , height=378, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
LogsFrame.place(x=116, y= 420)

#---------------- Config Frame --------------------
ConfigsFrame = ctk.CTkFrame(master=app , width=596 , height=798, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
ConfigsFrame.pack_propagate(False)
ConfigScrollBar = ctk.CTkScrollableFrame(master=ConfigsFrame, fg_color=rgb((19, 19, 54)))

ConfigScrollBar.pack(padx= 2 , pady= 2 , fill="both" , expand=True)
ConfigsFrame.place(x= 904, y= 2)

Frames = list()
selected_config_Frame : ctk.CTkFrame | None = None

def TopSelected():
    global selected_config_Frame
    if selected_config_Frame is Frames[0]:
        return

    selected_config_Frame.pack_forget()
    selected_config_Frame.pack(padx=2, pady=2 , side="top"  ,fill="x", expand=True, before=Frames[0])

    Frames.insert(0,Frames.pop(Frames.index(selected_config_Frame)))

def FrameConfiguration(frame : ctk.CTkFrame):
    def on_enter(event):
        frame.configure(fg_color=rgb((0, 74, 173)))

    def on_leave(event):
        global selected_config_Frame
        if frame is not selected_config_Frame:
            frame.configure(fg_color=rgb((19, 19, 54)))

    def on_press(event):
        frame.configure(fg_color=rgb((94, 23, 235)))

    def on_release(event):
        global selected_config_Frame
        x = event.x
        y = event.y

        width = frame.winfo_width()
        height = frame.winfo_height()

        if 0 <= x <= width and 0 <= y <= height:
            if selected_config_Frame is not None:
                selected_config_Frame.configure(fg_color=rgb((19, 19, 54)))
            if frame is not selected_config_Frame:
                selected_config_Frame = frame
                createSelectedConfigInfo()
            TopSelected()
            frame.configure(fg_color=rgb((0, 74, 173)))
        else:
            frame.configure(fg_color=rgb((24, 0, 173)))

    widgets = [frame] + frame.winfo_children()
    for widget in widgets:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<ButtonPress-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)

deleteImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "Delete.png") , size=(80,80))
deleteHoverImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "DeleteHover.png") , size=(80,80))
deleteClickedImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "DeleteClicked.png") , size=(80,80))

TagFont = ctk.CTkFont(family="Fredoka", size=30)
InfoFont = ctk.CTkFont(family="Fredoka", size=25)

def createConfigFrame(proxy: Proxy):
    configFrame = ctk.CTkFrame(master=ConfigScrollBar  , height=120, border_width=2 , border_color="white", fg_color=rgb((19, 19, 54)))
    configFrame.proxy = proxy

    ctk.CTkLabel(master=configFrame, text=proxy.display_tag , font=TagFont).place(x=5,y=5)
    ctk.CTkLabel(master=configFrame, text=proxy.protocol, font=InfoFont).place(x=10,y=60)
    ctk.CTkLabel(master=configFrame, text=proxy.port, font=InfoFont).place(x=100,y=60)

    FrameConfiguration(configFrame)
    DeleteButton = ctk.CTkButton(master=configFrame, width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
    buttonConfiguration(DeleteButton, deleteImage, deleteHoverImage, deleteClickedImage)
    DeleteButton.pack(side="right",padx=10,pady=10)
    Frames.append(configFrame)
    configFrame.pack(padx=2, pady=2 , side="top"  ,fill="x", expand=True)

def create_all(index=0):
    configs = Manager.Proxies

    if index >= len(configs):
        return

    createConfigFrame(configs[index])
    app.after(1, lambda: create_all(index + 1))


app.after(0, create_all)

def scroll_up(event):
    ConfigScrollBar._parent_canvas.yview_scroll(-1, "units")

def scroll_down(event):
    ConfigScrollBar._parent_canvas.yview_scroll(1, "units")

def bind_mousewheel(event=None):
    app.bind_all("<Button-4>", scroll_up)
    app.bind_all("<Button-5>", scroll_down)

def unbind_mousewheel(event=None):
    app.unbind_all("<Button-4>")
    app.unbind_all("<Button-5>")

ConfigScrollBar.bind("<Enter>", bind_mousewheel)
ConfigScrollBar.bind("<Leave>", unbind_mousewheel)

SelectedConfigInfo = ctk.CTkFrame(master=app , width=784 , height=796, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

def createSelectedConfigInfo():
    global SelectedConfigInfo
    global selected_config_Frame
    SelectedConfigInfo.pack_propagate(False)

    for widget in SelectedConfigInfo.winfo_children():
        widget.destroy()

    if selected_config_Frame is None:
        ctk.CTkLabel(master=SelectedConfigInfo, text="no configs selected!", font=TagFont).place(x=150 , y=150)
    else:
        ProxyInfo:dict = selected_config_Frame.proxy.to_dict()

        for row, (key, value) in enumerate(ProxyInfo.items()):
            if key == "tag" and value:
                value = selected_config_Frame.proxy.display_tag

            ctk.CTkLabel(master=SelectedConfigInfo,text=f"{key}:",font=InfoFont).place(x=10, y=10 + row * 40)

            if key == "extra_params" and isinstance(value, dict):
                for erow, (ekey, evalue) in enumerate(value.items()):
                    ctk.CTkLabel(master=SelectedConfigInfo,text=f"{ekey}:",font=InfoFont).place(x=40, y=300 + erow * 40)
                    ctk.CTkLabel(master=SelectedConfigInfo,text=str(evalue),font=InfoFont).place(x=190, y=300 + erow * 40)
                continue

            ctk.CTkLabel(master=SelectedConfigInfo,text=str(value),font=InfoFont).place(x=150, y=10 + row * 40)

    if current_page == "Configs":
        SelectedConfigInfo.place(x=116  , y=2)

#---------------- Routing Frame --------------------
routings_frame = routingFrame(app=app)

app.mainloop()