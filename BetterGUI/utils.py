import customtkinter as ctk
from PIL import Image
from pathlib import Path

root = Path(__file__).resolve().parent

def rgb(color):
    return "#%02x%02x%02x" % color

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