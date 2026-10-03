import customtkinter as ctk
from utils import rgb, root
from PIL import Image
from service import terminal

icons_directory = root / "icons"

class MainFrame:
    def __init__(self, app:ctk.CTk):
        self.MainFrame = ctk.CTkFrame(master=app, width=784 , height=300 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
        self.ConnectButton = ctk.CTkButton(master=self.MainFrame , width= 200, height=200 , text= "" , fg_color=rgb((19, 19, 54)))

        self.ConnectButtonConfiguration(
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

    def ConnectButtonConfiguration(self, Btn: ctk.CTkButton, StandardImage1: Image.Image, HoverImage1: Image.Image, ClickImage1: Image.Image, StandardImage2 : Image.Image, HoverImage2: Image.Image, ClickImage2: Image.Image, size=(200,200)):
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
                if Btn.Connected:
                    terminal.disable_v2ray()
                    Btn.Connected = False
                else:
                    terminal.enable_v2ray()
                    Btn.Connected = True
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
