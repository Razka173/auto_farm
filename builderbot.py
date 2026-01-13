import time as t
import customtkinter as ctk
import func as f
import threading
import attacks as a


p  = str(a.p) # port
Bbot_thread = None
Bbot_running = threading.Event()


def start_Bbot():
    global Bbot_thread
    if not Bbot_running.is_set():
        Bbot_thread = threading.Thread(target=BBot, daemon=True)
        Bbot_thread.start()
        log("BBot started.")

def stop_Bbot():
    Bbot_running.clear()
    log("Stopping Bbot...")




def BBot():
    Bbot_running.set()
    while Bbot_running.is_set():
        f.find(p)
        t.sleep(5)
        secondattack = False
        log("attack started")
        a.BB()
        t.sleep(10)
        while f.checkpixelBB(p,888,900) != "(180, 230, 125, 255)" :
            t.sleep(1)
            if f.checkpixelBB(p,1862,815) != "(255, 255, 255, 255)" and secondattack == False:
                secondattack = True
                log("round 2")
                a.BB2()
                t.sleep(10)
        
        log("attack finished")
        f.tap(950,900,p)
        t.sleep(2)
        f.swipe(p)
        log("collecting loot")
        t.sleep(0.5)
        f.tap(871,521,p)
        t.sleep(0.5)
        f.tap(1400,920,p)
        t.sleep(1)
        f.tap(1600,100,p)
        t.sleep(1)


# Create main window
App = ctk.CTk()        
App.title("CoC BBot")
App.geometry("700x400")  # Wider window to accommodate loot display

# Button frame
App.button_frame = ctk.CTkFrame(App)
App.button_frame.pack(pady=10)
        
App.button2 = ctk.CTkButton(App.button_frame, text="Start BBot", command=start_Bbot)
App.button2.grid(row=0, column=0, padx=5)
        
App.button3 = ctk.CTkButton(App.button_frame, text="Stop BBot", command=stop_Bbot)
App.button3.grid(row=0, column=1, padx=5)

# Main content frame
App.content_frame = ctk.CTkFrame(App)
App.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Log textbox
App.log_textbox = ctk.CTkTextbox(App.content_frame, height=200, wrap="word")
App.log_textbox.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

# Configure grid weights
App.content_frame.columnconfigure(0, weight=3)

App.content_frame.rowconfigure(0, weight=1)

def log(message):
    textbox = App.log_textbox._textbox
    textbox.tag_configure("spacing", spacing3=8)
    textbox.insert("end", message + "\n", "spacing")
    textbox.see("end")


App.mainloop()