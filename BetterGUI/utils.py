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

