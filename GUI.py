import tkinter as tk
from service import manager , terminal , proxy
from pathlib import Path

root_file = Path(__file__).resolve().parent

root = tk.Tk()

root.title("V2rayGUI")
root.geometry("600x600")
root.resizable(width=False, height=False)

manager.Manager.read_all()

config_scrollbar_frame = tk.Frame(root, borderwidth=2, relief="groove", background="gray")
config_scrollbar_frame.place(x=0, y=0, height=400, width=600)

canvas = tk.Canvas(config_scrollbar_frame, background="gray", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(config_scrollbar_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = tk.Frame(canvas, background="gray")
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

def update_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

inner_frame.bind("<Configure>", update_scroll)

def make_config_frame(prxy : proxy.Proxy):
    config_frame = tk.Frame(inner_frame, borderwidth=2 , relief="groove" , background="white" , height=30 , width=600)
    config_frame.pack(pady=2)
    config_frame.pack_propagate(False)

    label = tk.Label(config_frame , text=prxy.unquoted_tag)
    label.place(x=2 , y=0 , height=25 , width=398)

    select_button = tk.Button(config_frame, borderwidth=2 , relief="groove" , text="select" , command=lambda : manager.Manager.write(prxy, root_file/"data"/"config.json"))
    select_button.place(x=400 , y=0 , height=25 , width=90)

    def removeFrame():
        manager.Manager.remove(prxy)
        config_frame.destroy()

    delete_button = tk.Button(config_frame, borderwidth=2 , relief="groove" , text="delete" , command=removeFrame)
    delete_button.place(x=490 , y=0 , height=25 , width=90)

for prxy in manager.Manager.Proxies :
    make_config_frame(prxy)

UI_frame = tk.Frame(root , borderwidth=2 , relief="groove" , background="lightgray")
UI_frame.place(x=0 , y=400 , height=200 , width=600)

start_button = tk.Button(UI_frame , borderwidth=2 , relief="groove" , text="start" , background="gray")
start_button.place(x=10 , y=10 , height=80 , width=100)

def Start():
    terminal.enable_v2ray()
    start_button.configure(text="stop" , command=Stop)

def Stop():
    terminal.disable_v2ray()
    start_button.configure(text="start" , command=Start)

start_button.configure(command=Start)

textBox = tk.Text(UI_frame , borderwidth=2 , relief="groove" , background="white")
textBox.place(x=10 , y=100 , height=80 , width=480)

def add():
    url = textBox.get("1.0", tk.END).strip()

    if url == "":
        return
    
    try:
        prxy = proxy.Proxy.from_URL(url)
        manager.Manager.add(prxy)

    except Exception as e:
        return f'error : {e}'
    
    make_config_frame(prxy)

    textBox.delete("1.0", tk.END)

add_button = tk.Button(UI_frame , text="+" ,borderwidth=2 , relief="groove", background="gray" , command=add)
add_button.place(x=490 , y=100 , height=80 , width=100)

def on_close():
    manager.Manager.save()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()