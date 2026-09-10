import customtkinter as ctk
from rgb import rgb
from service.manager import Manager

TagFont = ctk.CTkFont(family="Fredoka", size=30)
InfoFont = ctk.CTkFont(family="Fredoka", size=25)

class routingFrame():
    def __init__(self, app: ctk.CTk):
        self.app = app
        self.Frame = ctk.CTkFrame(master=app, width=784 , height=300 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
        self.Frame.pack_propagate(False)
        self.scrollbar = ctk.CTkScrollableFrame(master=self.Frame, fg_color=rgb((19, 19, 54)))
        self.selected_profile = Manager.Routings["full_tunnel"]

        self.profile_frames = []


    def create_routing_profile_frame(self, name, index):
        profile_frame = ctk.CTkFrame(master=self.scrollbar, width=150, height=300, border_width=2, border_color="white", fg_color=rgb((19, 19, 54)))
        ctk.CTkLabel(master=profile_frame, text=name, font=TagFont).place(x=5,y=5)

        row = index // 3

        profile_frame.pack(row=row)
        self.profile_frames.append(profile_frame)

    def create_all(self, index=0):
        profiles = Manager.Routings

        if index >= len(profiles):
                return

        self.create_routing_profile_frame(profiles[index])
        self.app.after(1, lambda: self.create_all(index+1))