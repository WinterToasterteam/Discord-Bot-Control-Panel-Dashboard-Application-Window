"""
made by toasterteam and along with chatgpt for help!
also by the way, please make sure to put this INSIDE your bot project folder or else it might
not work like you expect to be.
install .wav files in the project folder for sounds.
install your .png logo so it can copy it off from there to here to create your bot logo.
"""
import tkinter as tk
import subprocess
import threading
import sys
import os
import winsound
import queue
import time
import psutil
import json

# ===== GLOBALS =====
bot_process = None
console_queue = queue.Queue()
console_window = None

# ===== HELPER =====
def resource_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# ===== PLAY STARTUP SOUND =====
def play_startup_sound():
    winsound.PlaySound(resource_path("StartupIntelPreT2Mac.wav"), winsound.SND_ASYNC) # this one is optional

threading.Thread(target=play_startup_sound).start()

# ===== MAIN WINDOW =====
root = tk.Tk()
root.title("Toastabot Dashboard") #rename it to your bot
root.geometry("900x600")
root.configure(bg="black")
root.resizable(False, False)
root.attributes("-alpha", 0.0)


try:
    icon_img = tk.PhotoImage(file=resource_path("toastabotpng.png")) #replace with your png logo
    root.iconphoto(True, icon_img)
except Exception as e:
    print("Window icon load error:", e)

# ===== LOADING SCREEN =====
loading_frame = tk.Frame(root, bg="black")
loading_frame.place(relwidth=1, relheight=1)

load_logo_img = tk.PhotoImage(file=resource_path("toastabotpng.png")) #replace with your png logo
loading_logo = tk.Label(loading_frame, image=load_logo_img, bg="black")
loading_logo.pack(pady=30)

loading_text = tk.Label(
    loading_frame,
    text="Initializing Toastabot…", #replace this with bot name
    fg="white",
    bg="black",
    font=("Segoe UI", 22)
)
loading_text.pack(pady=10)

# ===== DASHBOARD =====
dashboard_frame = tk.Frame(root, bg="black")

dash_logo = tk.Label(
    dashboard_frame,
    image=load_logo_img,
    bg="black"
)
dash_logo.pack(pady=10)

title_label = tk.Label(
    dashboard_frame,
    text="🍞 Toastabot Control Panel", #rename this part if you like to
    fg="white",
    bg="black",
    font=("Segoe UI", 26)
)
title_label.pack(pady=5)

status_label = tk.Label(
    dashboard_frame,
    text="Bot Status: OFFLINE",
    fg="white",
    bg="black",
    font=("Segoe UI", 18)
)
status_label.pack(pady=5)

# ===== CONSOLE WINDOW CREATION =====

def create_console_window():
    global console_window

    
    if console_window and console_window.winfo_exists():
        console_window.lift()
        return

 
    console_window = tk.Toplevel(root)
    console_window.title("Bot Console")
    console_window.geometry("900x350")
    console_window.configure(bg="black")
    console_window.attributes("-alpha", 0.0)

  
    try:
        console_window.iconphoto(True, icon_img)
    except Exception as e:
        print("Console icon load error:", e)

    console_text = tk.Text(console_window, bg="black", fg="cyan", font=("Consolas", 11))
    console_text.pack(expand=True, fill="both")
    console_text.config(state="disabled")

    def write_to_console(text):
        console_text.config(state="normal")
        console_text.insert(tk.END, text)
        console_text.see(tk.END)
        console_text.config(state="disabled")

   
    console_window.write_to_console = write_to_console

    fade_in_console()

# ===== BOT START / STOP =====

def start_bot():
    global bot_process
    if bot_process is None:
        bot_file = resource_path("bot.py") #replace file name to your main bot - toasterteam

        bot_process = subprocess.Popen(
            [sys.executable, "-u", bot_file],
            cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        status_label.config(text="Bot Status: RUNNING")
        threading.Thread(target=read_console_output, daemon=True).start()


def stop_bot():
    global bot_process

    if bot_process:
        pid = bot_process.pid
        try:
            
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F", "/T"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            print("Shutdown error:", e)

        bot_process = None
        status_label.config(text="Bot Status: OFFLINE")




def read_console_output():
    global bot_process
    while True:
        
        if bot_process is None:
            break

        
        try:
            output = bot_process.stdout.readline()
        except Exception:
            break

        if output:
            if console_window and console_window.winfo_exists():
                console_window.write_to_console(output)

        
        try:
            if bot_process.poll() is not None:
                if console_window and console_window.winfo_exists():
                    console_window.write_to_console("\n !! -- bot process ended -- !!\n")
                    console_window.write_to_console("\n!! // discord api might show it as online! if you recieve this message, the shutdown worked, its delayed in the discord api. // !!\n")
                status_label.config(text="Bot Status: OFFLINE")
                bot_process = None
                break
        except Exception:
            break

        time.sleep(0.01)


# ===== DASHBOARD BUTTONS =====

start_btn = tk.Button(
    dashboard_frame,
    text="start bot",
    command=start_bot,
    width=24,
    height=2,
    bg="#2E8B57",            # background color
    fg="white",              # text color
    activebackground="#246B45",  # color when clicked
    activeforeground="white",
    highlightthickness=0
)
start_btn.pack(pady=8)

stop_btn = tk.Button(
    dashboard_frame,
    text="shutdown bot",
    command=stop_bot,
    width=24,
    height=2,
    bg="#B22222",
    fg="white",
    activebackground="#8B1A1A",
    activeforeground="white",
    highlightthickness=0
)
stop_btn.pack(pady=8)

console_btn = tk.Button(
    dashboard_frame,
    text="open console",
    command=create_console_window,
    width=24,
    height=2,
    bg="#4682B4",
    fg="white",
    activebackground="#35698F",
    activeforeground="white",
    highlightthickness=0
)
console_btn.pack(pady=8)

latency_label = tk.Label(
    dashboard_frame,
    text="bot latency: n/a",
    fg="white",
    bg="black",
    font=("Segoe UI", 18)
)
latency_label.pack(pady=5)

# ===== LATENCY SYSTEM =====
def update_latency_display():
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    latency_path = os.path.join(bot_dir, "latency.json") #replace file name to your latency.json or atleast copy the name and make one - toasterteam
    # oh yeah by the way make sure to ACTUALLY put a dict: {} inside your latency.json file
    try:
        if os.path.exists(latency_path):
            with open(latency_path, "r") as f:
                data = json.load(f)
                latency = data.get("latency")
                if latency is not None:
                    latency_label.config(text=f"bot latency: {latency} ms")
                else:
                    latency_label.config(text="bot latency: n/a")
        else:
            latency_label.config(text="bot latency: n/a")
    except Exception:
        latency_label.config(text="bot latency: error")

    root.after(1000, update_latency_display)  

# ===== FADE HELPERS =====

def fade_in(widget, step=0.05):
    alpha = widget.attributes("-alpha")
    new_alpha = min(alpha + step, 1.0)
    widget.attributes("-alpha", new_alpha)
    if new_alpha < 1.0:
        widget.after(30, lambda: fade_in(widget, step))

def fade_out_then_show():
    alpha = root.attributes("-alpha")
    new_alpha = max(alpha - 0.05, 0.0)
    root.attributes("-alpha", new_alpha)
    if new_alpha > 0:
        root.after(30, fade_out_then_show)
    else:
        loading_frame.place_forget()
        dashboard_frame.place(relwidth=1, relheight=1)
        fade_in(root)


def fade_in_console(step=0.05, delay=30):
    if not console_window:
        return
    def inner():
        alpha = console_window.attributes("-alpha")
        new_alpha = min(alpha + step, 1.0)
        console_window.attributes("-alpha", new_alpha)
        if new_alpha < 1.0:
            console_window.after(delay, inner)
    inner()

# ===== TRANSITION =====

root.after(3000, fade_out_then_show)
fade_in(root)

update_latency_display()

root.mainloop()
