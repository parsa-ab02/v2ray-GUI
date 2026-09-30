import customtkinter as ctk
from utils import rgb
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from service.manager import Manager

class routingFrame():
    def __init__(self, app: ctk.CTk):
        self.app = app
        self.Frame = ctk.CTkFrame(master=app, width=784 , height=796 , border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
        self.Frame.pack_propagate(False)
        self.scrollbar = ctk.CTkScrollableFrame(master=self.Frame, fg_color=rgb((19, 19, 54)))
        self.scrollbar.pack(padx= 2, pady= 2, fill="both", expand=True)
        self.name_font = ctk.CTkFont(family="Fredoka", size=30)
        self.info_font = ctk.CTkFont(family="Fredoka", size=18)
        # self.selected_profile = Manager.Routings["full_tunnel"]
        self.selected_profile_frame: ctk.CTkFrame | None = None

        self.profile_frames = []

    def Routing_profile_configuration(self, frame: ctk.CTkFrame):
        def on_enter(event):
            frame.configure(fg_color=rgb((0, 74, 173)))

        def on_leave(event):
            if frame is not self.selected_profile_frame:
                frame.configure(fg_color=rgb((19, 19, 54)))

        def on_press(event):
            frame.configure(fg_color=rgb((94, 23, 235)))

        def on_release(event):
            x = event.x
            y = event.y

            width = frame.winfo_width()
            height = frame.winfo_height()

            if 0 <= x <= width and 0 <= y <= height:
                if self.selected_profile_frame is not None:
                    self.selected_profile_frame.configure(fg_color=rgb((19, 19, 54)))
                if frame is not self.selected_profile_frame:
                    self.selected_profile_frame = frame
                frame.configure(fg_color=rgb((0, 74, 173)))
            else :
                frame.configure(fg_color=rgb((24, 0, 173)))

            # if frame is not self.selected_profile_frame:
            #     if self.selected_profile_frame is not None:
            #         self.selected_profile_frame.configure(fg_color=rgb((19, 19, 54)))

            #     self.selected_profile_frame = frame

            #     frame.configure(fg_color=rgb((0, 74, 173)))

        widgets = [frame] + frame.winfo_children()

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<ButtonPress-1>", on_press)
            widget.bind("<ButtonRelease-1>", on_release)


    def create_routing_profile_frame(self, name, routing_dict, index):
        profile_frame = ctk.CTkFrame(master=self.scrollbar,width=243,height=250,border_width=2,border_color="white",fg_color=rgb((19, 19, 54)))
        ctk.CTkLabel(master=profile_frame,text=name, font=self.name_font).place(x=5, y=10)

        current_y = 50
        for key, value in routing_dict.items():
            if current_y + 30 > 250:
                break

            if not isinstance(value, list):
                ctk.CTkLabel(master=profile_frame,text=f"{key}:", font=self.info_font).place(x=10, y=current_y)
                ctk.CTkLabel(master=profile_frame,text=str(value)).place(x=130, y=current_y)

                current_y += 30

            else:
                ctk.CTkLabel(master=profile_frame,text=f"{key}:", font=self.info_font).place(x=10, y=current_y)

                current_y += 30
                for rule_dict in value:
                    for ekey, evalue in rule_dict.items():
                        if current_y + 25 > 240:
                            break

                        ctk.CTkLabel(master=profile_frame,text=f"{ekey}:", font=self.info_font).place(x=20,y=current_y)
                        ctk.CTkLabel(master=profile_frame,text=str(evalue), font=self.info_font).place(x=110,y=current_y)

                        current_y += 25
                    current_y += 5
        row = index // 3
        column = index % 3

        self.Routing_profile_configuration(profile_frame)
        profile_frame.grid(row=row,column=column,padx=5,pady=5)
        self.profile_frames.append(profile_frame)

    def create_all(self, index=0):
        profiles = Manager.Routings

        if index >= len(profiles):
                return

        self.create_routing_profile_frame(list(profiles.keys())[index], list(profiles.values())[index], index)
        self.app.after(1, lambda: self.create_all(index+1))

    def show(self):
        self.create_all()
        self.Frame.place(x=116 , y= 2)

    def remove(self):
        self.Frame.place_forget()