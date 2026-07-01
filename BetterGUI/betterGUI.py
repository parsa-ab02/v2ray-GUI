import customtkinter as ctk
from pathlib import Path
from PIL import Image
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import service.config

root = Path(__file__).resolve().parent
icons_directory = root / "icons"

service.config.Config.read_all()

def rgb(color):
    return "#%02x%02x%02x" % color

current_page = "Home"
def ShowHome():
    global current_page
    if current_page != "Home":
        SelectedConfigInfo.place_forget()
        MainFrame.place(x=116 , y= 2)
        AddFrame.place(x= 116,y= 306)
        ConfigsFrame.place_forget()
        ConfigsFrame.configure(width=596)
        ConfigsFrame.place(x= 904, y= 2)
        LogsFrame.place(x=116, y= 420)
        current_page = "Home"

def ShowConfigs():
    global current_page
    if current_page != "Configs":
        MainFrame.place_forget()
        AddFrame.place_forget()
        LogsFrame.place_forget()
        ConfigsFrame.place_forget()
        ConfigsFrame.configure(width=800)
        ConfigsFrame.place(x=116 , y= 2)
        current_page = "Configs"
        createSelectedConfigInfo()

def ShowRouting():
    pass

def ShowLogs():
    pass

def ShowSettings():
    pass


def buttonConfiguration(Btn: ctk.CTkButton, StandardImage: ctk.CTkImage, HoverImage: ctk.CTkImage, ClickImage: ctk.CTkImage, command=None):
    Btn.standard_image = StandardImage
    Btn.hover_image = HoverImage
    Btn.click_image = ClickImage

    Btn.configure(text="", image=Btn.standard_image,fg_color=rgb((24, 0, 173)) ,hover= False)

    def on_enter(event):
        Btn.configure(image=Btn.hover_image, fg_color=rgb((0, 74, 173)))

    def on_leave(event):
        Btn.configure(image=Btn.standard_image, fg_color=rgb((24, 0, 173)))

    def on_press(event):
        Btn.configure(image=Btn.click_image, fg_color=rgb((94, 23, 235)))

    def on_release(event):
        x = event.x
        y = event.y

        width = Btn.winfo_width()
        height = Btn.winfo_height()

        if 0 <= x <= width and 0 <= y <= height:
            Btn.configure(image=Btn.hover_image, fg_color=rgb((0, 74, 173)))
            if command is not None:
                command()
        else:
            Btn.configure(image=Btn.standard_image, fg_color=rgb((24, 0, 173)))

    Btn.bind("<Enter>", on_enter)
    Btn.bind("<Leave>", on_leave)
    Btn.bind("<ButtonPress-1>", on_press)
    Btn.bind("<ButtonRelease-1>", on_release)


app = ctk.CTk()
app.title("v2ray GUI")
app.geometry("1500x800")
app.resizable(width=False , height=False)
ctk.set_appearance_mode("dark")

# -------------- Side Frame ----------------------

SideFrame = ctk.CTkFrame(master=app , width=110 , height=798 , fg_color=rgb((19, 19, 54)) ,border_width=2 , border_color="white")

HomeButton = ctk.CTkButton(master = SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(HomeButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Home.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "HomeHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "HomeClicked.png"), size=(80,80)) , command=ShowHome)
HomeButton.place(x=4,y=4)

ConfigsButton = ctk.CTkButton(master = SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(ConfigsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Configs.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ConfigsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "ConfigsClicked.png"), size=(80,80)) , command=ShowConfigs)
ConfigsButton.place(x=4 , y=106)

RoutingButton = ctk.CTkButton(master = SideFrame ,width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(RoutingButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Routing.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "RoutingHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "RoutingClicked.png"), size=(80,80)))
RoutingButton.place(x=4 , y= 208)

LogsButton = ctk.CTkButton(master = SideFrame ,width=100 ,text= "",fg_color=rgb((24, 0, 173)) , hover_color=rgb((24, 0, 173)),  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(LogsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Logs.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "LogsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "LogsClicked.png"), size=(80,80)))
LogsButton.place(x=4 , y= 310)

SettingsButton = ctk.CTkButton(master = SideFrame ,width=100 ,text= "",fg_color=rgb((24, 0, 173)) , hover_color=rgb((24, 0, 173)),  height=100 , border_width=2 , border_color="white" , corner_radius=10)
buttonConfiguration(SettingsButton , ctk.CTkImage(dark_image=Image.open(icons_directory / "Settings.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "SettingsHover.png"), size=(80,80)) , ctk.CTkImage(dark_image=Image.open(icons_directory / "SettingsClicked.png"), size=(80,80)))
SettingsButton.place(x=4 , y = 696)

SideFrame.place(x = 2 , y = 2)
# --------------- Main Frame ----------------------

MainFrame = ctk.CTkFrame(master=app, width=784 , height=300 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

ConnectButton = ctk.CTkButton(master=MainFrame , width= 200, height=200 , text= "" , fg_color=rgb((19, 19, 54)))

def ConnectButtonConfiguration(Btn: ctk.CTkButton, StandardImage1: Image.Image, HoverImage1: Image.Image, ClickImage1: Image.Image, StandardImage2 : Image.Image, HoverImage2: Image.Image, ClickImage2: Image.Image, size=(200,200)):
    standard1_ctk_image = ctk.CTkImage(dark_image=StandardImage1, size=size)
    hover1_ctk_image = ctk.CTkImage(dark_image=HoverImage1, size=size)
    click1_ctk_image = ctk.CTkImage(dark_image=ClickImage1, size=size)
    standard2_ctk_image = ctk.CTkImage(dark_image=StandardImage2, size=size)
    hover2_ctk_image = ctk.CTkImage(dark_image=HoverImage2, size=size)
    click2_ctk_image = ctk.CTkImage(dark_image=ClickImage2, size=size)

    Btn.Connected = False
    Btn.standard1_image = standard1_ctk_image
    Btn.hover1_image = hover1_ctk_image
    Btn.click1_image = click1_ctk_image
    Btn.standard2_image = standard2_ctk_image
    Btn.hover2_image = hover2_ctk_image
    Btn.click2_image = click2_ctk_image
    Btn.isPressed = False


    Btn.configure(text="", image=Btn.standard1_image,hover= False)

    def is_inside_circle(x, y):
        width = Btn.winfo_width()
        height = Btn.winfo_height()
        return (x-(width/2))**2 + (y-(height/2))**2 <= 100**2

    def show_standard():
        if Btn.Connected:
            Btn.configure(image=Btn.standard2_image)
        else:
            Btn.configure(image=Btn.standard1_image)

    def show_hover():
        if Btn.Connected:
            Btn.configure(image=Btn.hover2_image)
        else:
            Btn.configure(image=Btn.hover1_image)

    def show_click():
        Btn.isPressed = True
        if Btn.Connected:
            Btn.configure(image=Btn.click2_image)
        else:
            Btn.configure(image=Btn.click1_image)

    def on_enter(event):
        if is_inside_circle(event.x, event.y):
            show_hover()
        else:
            show_standard()

    def on_leave(event):
        show_standard()

    def on_press(event):
        if is_inside_circle(event.x, event.y):
            show_click()
        else:
            show_standard()

    def on_release(event):
        Btn.isPressed = False
        if is_inside_circle(event.x, event.y):
            Btn.Connected = not Btn.Connected
            show_hover()
        else:
            show_standard()

    def on_motion(event):
        if is_inside_circle(event.x, event.y):
            if Btn.isPressed :
                show_click()
            else :
                show_hover()
        else:
            show_standard()

    Btn.bind("<Enter>", on_enter)
    Btn.bind("<Leave>", on_leave)
    Btn.bind("<Motion>", on_motion)
    Btn.bind("<ButtonPress-1>", on_press)
    Btn.bind("<ButtonRelease-1>", on_release)

ConnectButtonConfiguration(ConnectButton, Image.open(icons_directory / "Connect.png") , Image.open(icons_directory / "ConnectHover.png") , Image.open(icons_directory / "ConnectClicked.png"),
                           Image.open(icons_directory / "Connected.png") , Image.open(icons_directory / "ConnectedHover.png") , Image.open(icons_directory / "ConnectedClicked.png"))

StatusLabel = ctk.CTkLabel(master=MainFrame, text="Status : Not Connected" , font=ctk.CTkFont(family="Fredoka", size=30)).place(x=280,y=50)
DownLinkLabel = ctk.CTkLabel(master=MainFrame, text="DownLink" , font=ctk.CTkFont(family="Fredoka", size=30)).place(x=280,y=100)
DownLinkLabel = ctk.CTkLabel(master=MainFrame, text="UpLink" , font=ctk.CTkFont(family="Fredoka", size=30)).place(x=450,y=100)
ConnectButton.place(x= 10 , y= 50)
MainFrame.place(x=116 , y= 2)
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
selectedFrame : ctk.CTkFrame | None = None

def TopSelected():
    global selectedFrame
    if selectedFrame is Frames[0]:
        return

    selectedFrame.pack_forget()
    selectedFrame.pack(padx=2, pady=2 , side="top"  ,fill="x", expand=True, before=Frames[0])

    Frames.insert(0,Frames.pop(Frames.index(selectedFrame)))

def FrameConfiguration(frame : ctk.CTkFrame):
    def on_enter(event):
        frame.configure(fg_color=rgb((0, 74, 173)))

    def on_leave(event):
        global selectedFrame
        if frame is not selectedFrame:
            frame.configure(fg_color=rgb((19, 19, 54)))

    def on_press(event):
        frame.configure(fg_color=rgb((94, 23, 235)))

    def on_release(event):
        global selectedFrame
        x = event.x
        y = event.y

        width = frame.winfo_width()
        height = frame.winfo_height()

        if 0 <= x <= width and 0 <= y <= height:
            if selectedFrame is not None:
                selectedFrame.configure(fg_color=rgb((19, 19, 54)))
            if frame is not selectedFrame:
                selectedFrame = frame
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

def createConfigFrame(config):
    configFrame = ctk.CTkFrame(master=ConfigScrollBar  , height=120, border_width=2 , border_color="white", fg_color=rgb((19, 19, 54)))
    configFrame.conf = config
    TagLabel = ctk.CTkLabel(master=configFrame, text=config.tag , font=TagFont)
    ProtocolLabel = ctk.CTkLabel(master=configFrame, text=config.protocol, font=InfoFont)
    PortLabel = ctk.CTkLabel(master=configFrame, text=config.port, font=InfoFont)
    TagLabel.place(x=5,y=5)
    ProtocolLabel.place(x=10,y=60)
    PortLabel.place(x=100,y=60)
    FrameConfiguration(configFrame)
    DeleteButton = ctk.CTkButton(master=configFrame, width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
    buttonConfiguration(DeleteButton, deleteImage, deleteHoverImage, deleteClickedImage)
    DeleteButton.pack(side="right",padx=10,pady=10)
    Frames.append(configFrame)
    configFrame.pack(padx=2, pady=2 , side="top"  ,fill="x", expand=True)

def create_all(index=0):
    configs = service.config.Config.config_list

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

SelectedConfigInfo = ctk.CTkFrame(master=app , width=576 , height=400, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

def createSelectedConfigInfo():
    global SelectedConfigInfo
    global selectedFrame
    SelectedConfigInfo.pack_propagate(False)
    for widget in SelectedConfigInfo.winfo_children():
        widget.destroy()
    if selectedFrame is None:
        emptyLabel = ctk.CTkLabel(master=SelectedConfigInfo, text="no configs selected!", font=TagFont).place(x=150 , y=150)
    else:
        TagLabel = ctk.CTkLabel(master=SelectedConfigInfo, text=selectedFrame.conf.tag , font=TagFont).place(x= 10 , y= 10)
        ProtocolLabel = ctk.CTkLabel(master=SelectedConfigInfo, text=f"protocol : {selectedFrame.conf.protocol}", font=InfoFont).place(x= 10 , y= 50)
        PortLabel = ctk.CTkLabel(master=SelectedConfigInfo, text=f"port : {selectedFrame.conf.port}", font=InfoFont).place(x= 210 , y= 50)
        hostNameLabel = ctk.CTkLabel(master=SelectedConfigInfo, text=f"host name :{selectedFrame.conf.ParsedUrl.hostname}", font=InfoFont).place(x= 10 , y= 100)
        URLLabel = ctk.CTkLabel(master=SelectedConfigInfo, text=selectedFrame.conf.raw_url, font=InfoFont).place(x= 10 , y= 150)

    if current_page == "Configs":
        SelectedConfigInfo.place(x=920  , y=2)

app.mainloop()