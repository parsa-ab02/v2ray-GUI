import customtkinter as ctk
from utils import rgb, root, buttonConfiguration
from PIL import Image
from service.proxy import Proxy
from service.manager import Manager

icons_directory = root / "icons"

class ConfigsFrame:
    def __init__(self, app: ctk.CTk):
        self.app = app
        self.ConfigsFrame = ctk.CTkFrame(master=app , width=596 , height=798, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))
        self.ConfigsFrame.pack_propagate(False)
        self.ConfigScrollBar = ctk.CTkScrollableFrame(master=self.ConfigsFrame, fg_color=rgb((19, 19, 54)))

        self.ConfigScrollBar.pack(padx= 2 , pady= 2 , fill="both" , expand=True)

        self.Frames = list()
        self.selected_config_Frame : ctk.CTkFrame | None = None

        self.deleteImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "Delete.png") , size=(80,80))
        self.deleteHoverImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "DeleteHover.png") , size=(80,80))
        self.deleteClickedImage = ctk.CTkImage(dark_image=Image.open(icons_directory / "DeleteClicked.png") , size=(80,80))

        self.TagFont = ctk.CTkFont(family="Fredoka", size=30)
        self.InfoFont = ctk.CTkFont(family="Fredoka", size=25)

        self.SelectedConfigInfo = ctk.CTkFrame(master=app , width=784 , height=796, border_width=2 , border_color="white" , fg_color=rgb((19, 19, 54)))

    def TopSelected(self):
        if self.selected_config_Frame is self.Frames[0]:
            return

        self.selected_config_Frame.pack_forget()
        self.selected_config_Frame.pack(
            padx=2, pady=2,
            side="top"  ,fill="x",
            expand=True, before=self.Frames[0]
        )

        self.Frames.insert(0,self.Frames.pop(self.Frames.index(self.selected_config_Frame)))

    def FrameConfiguration(self, frame : ctk.CTkFrame):
        def on_enter(event):
            frame.configure(fg_color=rgb((0, 74, 173)))

        def on_leave(event):
            if frame is not self.selected_config_Frame:
                frame.configure(fg_color=rgb((19, 19, 54)))

        def on_press(event):
            frame.configure(fg_color=rgb((94, 23, 235)))

        def on_release(event):
            x = event.x
            y = event.y

            width = frame.winfo_width()
            height = frame.winfo_height()

            if 0 <= x <= width and 0 <= y <= height:
                if self.selected_config_Frame is not None:
                    self.selected_config_Frame.configure(fg_color=rgb((19, 19, 54)))
                if frame is not self.selected_config_Frame:
                    self.selected_config_Frame = frame
                    self.create_selected_config_info()
                self.TopSelected()
                frame.configure(fg_color=rgb((0, 74, 173)))
            else:
                frame.configure(fg_color=rgb((24, 0, 173)))

        widgets = [frame] + frame.winfo_children()
        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<ButtonPress-1>", on_press)
            widget.bind("<ButtonRelease-1>", on_release)

    def create_selected_config_info(self):
        self.SelectedConfigInfo.pack_propagate(False)

        for widget in self.SelectedConfigInfo.winfo_children():
            widget.destroy()

        if self.selected_config_Frame is None:
            ctk.CTkLabel(master=self.SelectedConfigInfo, text="no configs selected!", font=self.TagFont).place(x=150 , y=150)
        else:
            ProxyInfo:dict = self.selected_config_Frame.proxy.to_dict()

            for row, (key, value) in enumerate(ProxyInfo.items()):
                if key == "tag" and value:
                    value = self.selected_config_Frame.proxy.display_tag

                ctk.CTkLabel(master=self.SelectedConfigInfo,text=f"{key}:",font=self.InfoFont).place(x=10, y=10 + row * 40)

                if key == "extra_params" and isinstance(value, dict):
                    for erow, (ekey, evalue) in enumerate(value.items()):
                        ctk.CTkLabel(master=self.SelectedConfigInfo,text=f"{ekey}:",font=self.InfoFont).place(x=40, y=300 + erow * 40)
                        ctk.CTkLabel(master=self.SelectedConfigInfo,text=str(evalue),font=self.InfoFont).place(x=190, y=300 + erow * 40)
                    continue

                ctk.CTkLabel(master=self.SelectedConfigInfo,text=str(value),font=self.InfoFont).place(x=150, y=10 + row * 40)


    def create_config_frame(self, proxy: Proxy):
        configFrame = ctk.CTkFrame(master=self.ConfigScrollBar  , height=120, border_width=2 , border_color="white", fg_color=rgb((19, 19, 54)))
        configFrame.proxy = proxy

        ctk.CTkLabel(master=configFrame, text=proxy.display_tag , font=self.TagFont).place(x=5,y=5)
        ctk.CTkLabel(master=configFrame, text=proxy.protocol, font=self.InfoFont).place(x=10,y=60)
        ctk.CTkLabel(master=configFrame, text=proxy.port, font=self.InfoFont).place(x=100,y=60)

        self.FrameConfiguration(configFrame)
        DeleteButton = ctk.CTkButton(master=configFrame, width=100 ,text= "",  height=100 , border_width=2 , border_color="white" , corner_radius=10)
        buttonConfiguration(DeleteButton, self.deleteImage, self.deleteHoverImage, self.deleteClickedImage)
        DeleteButton.pack(side="right",padx=10,pady=10)
        self.Frames.append(configFrame)
        configFrame.pack(padx=2, pady=2 , side="top"  ,fill="x", expand=True)

    def create_all(self, index=0):
        configs = Manager.Proxies

        if index >= len(configs):
            return

        self.create_config_frame(configs[index])
        self.app.after(1, lambda: self.create_all(index + 1))

    def show(self):
        self.ConfigsFrame.place(x= 904, y= 2)
        self.app.after(0, self.create_all)

    def show_selected_config_info(self):
        self.create_selected_config_info()
        self.SelectedConfigInfo.place(x=116  , y=2)

    def remove_selected_config_info(self):
        self.SelectedConfigInfo.place_forget()

    def scroll_up(self, event):
        self.ConfigScrollBar._parent_canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.ConfigScrollBar._parent_canvas.yview_scroll(1, "units")

    def bind_mousewheel(self, event=None):
        self.app.bind_all("<Button-4>", self.scroll_up)
        self.app.bind_all("<Button-5>", self.scroll_down)

    def unbind_mousewheel(self, event=None):
        self.app.unbind_all("<Button-4>")
        self.app.unbind_all("<Button-5>")

        self.ConfigScrollBar.bind("<Enter>", self.bind_mousewheel)
        self.ConfigScrollBar.bind("<Leave>", self.unbind_mousewheel)