import time as t
import customtkinter as ctk
import func as f
import threading
import attacks as a
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

attacktype = "TapTap"

# Fetch port from environment variable or use default from attacks.py
p  = os.getenv("BOT_PORT", '5555')  # Default to the value from attacks.py if BOT_PORT is not set
bot_thread = None
bot_running = threading.Event()

def start_bot():
    global bot_thread
    if not bot_running.is_set():
        bot_thread = threading.Thread(target=loop, daemon=True)
        bot_thread.start()
        app.log("Bot started.")

def stop_bot():
    bot_running.clear()
    app.log("Stopping bot...")

def loop():
    bot_running.set()

    while bot_running.is_set():
        # Fetch dynamic target values from the GUI
        app.log("Fetching target values from GUI...")
        targets = app.get_targets()  # Fetch dynamic values
        gold_target = targets["gold_target"]
        elixir_target = targets["elixir_target"]
        dark_elixir_target = targets["dark_elixir_target"]
        gold_remaining = targets["gold_remaining"]
        elixir_remaining = targets["elixir_remaining"]
        dark_elixir_remaining = targets["dark_elixir_remaining"]
        troop_slots = targets["troop_slots"]
        heroes_slots = targets["heroes_slots"]
        spell_slots = targets["spell_slots"]
        gold_target_enabled = targets["gold_target_enabled"]
        elixir_target_enabled = targets["elixir_target_enabled"]
        dark_elixir_target_enabled = targets["dark_elixir_target_enabled"]

        attack_params = {
            "troop_slots": troop_slots,
            "heroes_slots": heroes_slots,
            "spell_slots": spell_slots,
        }

        # do detect state
        f.check_current_state(p)
        if f.check_current_state.is_lost_connection:
            f.tap(465, 524, p)
        if f.check_current_state.is_another_connect:
            f.tap(458, 519, p)
        if f.check_current_state.is_star_bonus:
            f.tap(814, 768, p)

        app.log("Searching for base...")
        f.find(p)
        t.sleep(6)
        f.check_loot(p)

        allow_attack = False
        finish_attack = False

        cond1 = cond2 = cond3 = True
        if (gold_target_enabled):
            cond1 = int(f.check_loot.result[0]) > gold_target
        if (elixir_target_enabled):
            cond2 = int(f.check_loot.result[1]) > elixir_target
        if (dark_elixir_target_enabled):
            cond3 = int(f.check_loot.result[2]) > dark_elixir_target

        # check loot state
        while ((not cond1 or not cond2 or not cond3) and bot_running.is_set()):
            # do detect state
            f.check_current_state(p)
            if f.check_current_state.is_lost_connection:
                f.tap(465, 524, p)
            if f.check_current_state.is_another_connect:
                f.tap(458, 519, p)
            if f.check_current_state.is_star_bonus:
                f.tap(814, 768, p)

            app.log("base found: " +  format(int(f.check_loot.result[0]), ",") + " Gold   " \
                + format(int(f.check_loot.result[1]), ",") + " Elixir   " \
                +  format(int(f.check_loot.result[2]), ",") + " Dark Elixir"
            )
            app.log("loot below target, going to next base")
            f.next(p)
            t.sleep(6)
            f.check_loot(p) # recursive loot check

            cond1 = cond2 = cond3 = True
            if (gold_target_enabled):
                cond1 = int(f.check_loot.result[0]) > gold_target
            if (elixir_target_enabled):
                cond2 = int(f.check_loot.result[1]) > elixir_target
            if (dark_elixir_target_enabled):
                cond3 = int(f.check_loot.result[2]) > dark_elixir_target

        allow_attack = True
        # attack state
        if bot_running.is_set() and allow_attack:
            app.log("base found: " +  format(int(f.check_loot.result[0]), ",") + " Gold   " \
                + format(int(f.check_loot.result[1]), ",") + " Elixir   " \
                +  format(int(f.check_loot.result[2]), ",") + " Dark Elixir"
            )
            app.log("attacking...")
            do_attack = getattr(a, attacktype)
            do_attack(params=attack_params)
            app.log("attack deployed, waiting for battle to finish")
            t.sleep(9)
            finish_attack = True

        
        # # check loot during attack
        # if bot_running.is_set():
        #     app.log("checking loot during attack")
        #     f.check_loot(p)
        #     recurring = 0
        #     while (
        #         int(f.check_loot.result[0]) > gold_remaining and 
        #         int(f.check_loot.result[1]) > elixir_remaining and 
        #         int(f.check_loot.result[2]) > dark_elixir_remaining
        #     ) and bot_running.is_set():
        #         # if loot is still above remaining threshold, continue attack
        #         t.sleep(2)
        #         f.check_loot(p)
        #         recurring += 1
        #         if recurring >= 3:
        #             return_home = f.check_return_home(p)
        #             app.log("return home check: " + str(return_home))
        #             if return_home == True:
        #                 break

        app.log("stopping attack, returning to base")
        if bot_running.is_set() and finish_attack:
            app.log("returning")
            t.sleep(2)
            f.tap(800,770,p)
            t.sleep(5)

#################################################################################################### 
# Create main window
class ClasherControls:
    def __init__(self):
        self.App = ctk.CTk()
        self.App.title("Otomatisasi Robot CoC")
        self.App.geometry("720x600")  # Adjusted height for new fields

        # Button frame
        self.App.button_frame = ctk.CTkFrame(self.App)
        self.App.button_frame.pack(pady=10)

        self.App.button2 = ctk.CTkButton(self.App.button_frame, text="Start Bot", command=start_bot)
        self.App.button2.grid(row=0, column=0, padx=10, pady=5)  # Increased padding

        self.App.button3 = ctk.CTkButton(self.App.button_frame, text="Stop Bot", command=stop_bot)
        self.App.button3.grid(row=0, column=1, padx=10, pady=5)  # Increased padding

        # Main content frame
        self.App.content_frame = ctk.CTkFrame(self.App)
        self.App.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Log textbox
        self.App.log_textbox = ctk.CTkTextbox(self.App.content_frame, height=200, wrap="word")
        self.App.log_textbox.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)  # Increased padding

        # Configure grid weights
        self.App.content_frame.columnconfigure(0, weight=3)
        self.App.content_frame.rowconfigure(0, weight=1)

        # Loot target fields
        self.App.target_frame = ctk.CTkFrame(self.App)
        self.App.target_frame.pack(pady=10)

        self.var_is_gold = ctk.BooleanVar(value=True)
        self.var_is_elixir = ctk.BooleanVar(value=True)
        self.var_is_dark_elixir = ctk.BooleanVar(value=True)

        # First column
        ctk.CTkLabel(self.App.target_frame, text="Gold Target:").grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.gold_target_entry = ctk.CTkEntry(self.App.target_frame)
        self.gold_target_entry.insert(0, "250000")  # Default value
        self.gold_target_entry.grid(row=0, column=1, padx=10, pady=5)  # Increased padding

        self.gold_target_check = ctk.CTkCheckBox(self.App.target_frame, text="Enable", command=self.toggle_gold_target, variable=self.var_is_gold, onvalue=True, offvalue=False)
        self.gold_target_check.grid(row=0, column=2, padx=10, pady=5)  # Increased padding

        ctk.CTkLabel(self.App.target_frame, text="Elixir Target:").grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.elixir_target_entry = ctk.CTkEntry(self.App.target_frame)
        self.elixir_target_entry.insert(0, "250000")  # Default value
        self.elixir_target_entry.grid(row=1, column=1, padx=10, pady=5)  # Increased padding

        self.elixir_target_check = ctk.CTkCheckBox(self.App.target_frame, text="Enable", command=self.toggle_elixir_target, variable=self.var_is_elixir, onvalue=True, offvalue=False)
        self.elixir_target_check.grid(row=1, column=2, padx=10, pady=5)  # Increased padding

        ctk.CTkLabel(self.App.target_frame, text="Dark Elixir Target:").grid(row=2, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.dark_elixir_target_entry = ctk.CTkEntry(self.App.target_frame)
        self.dark_elixir_target_entry.insert(0, "500")  # Default value
        self.dark_elixir_target_entry.grid(row=2, column=1, padx=10, pady=5)  # Increased padding

        self.dark_elixir_target_check = ctk.CTkCheckBox(self.App.target_frame, text="Enable", command=self.toggle_dark_elixir_target, variable=self.var_is_dark_elixir, onvalue=True, offvalue=False)
        self.dark_elixir_target_check.grid(row=2, column=2, padx=10, pady=5)  # Increased padding

        # Second column
        ctk.CTkLabel(self.App.target_frame, text="Gold Threshold:").grid(row=0, column=3, padx=10, pady=5, sticky="w")  # Increased padding
        self.gold_remaining_entry = ctk.CTkEntry(self.App.target_frame)
        self.gold_remaining_entry.insert(0, "50000")  # Default value
        self.gold_remaining_entry.grid(row=0, column=4, padx=10, pady=5)  # Increased padding

        ctk.CTkLabel(self.App.target_frame, text="Elixir Threshold:").grid(row=1, column=3, padx=10, pady=5, sticky="w")  # Increased padding
        self.elixir_remaining_entry = ctk.CTkEntry(self.App.target_frame)
        self.elixir_remaining_entry.insert(0, "50000")  # Default value
        self.elixir_remaining_entry.grid(row=1, column=4, padx=10, pady=5)  # Increased padding

        ctk.CTkLabel(self.App.target_frame, text="Dark Elixir Threshold:").grid(row=2, column=3, padx=10, pady=5, sticky="w")  # Increased padding
        self.dark_elixir_remaining_entry = ctk.CTkEntry(self.App.target_frame)
        self.dark_elixir_remaining_entry.insert(0, "50")  # Default value
        self.dark_elixir_remaining_entry.grid(row=2, column=4, padx=10, pady=5)  # Increased padding

        # Troop and Heroes Slots
        # troop
        ctk.CTkLabel(self.App.target_frame, text="Troop Slot(s):").grid(row=3, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.troop_slots_entry = ctk.CTkEntry(self.App.target_frame)
        self.troop_slots_entry.insert(0, "1")  # Default value
        self.troop_slots_entry.grid(row=3, column=1, padx=10, pady=5)  # Increased padding

        ctk.CTkLabel(self.App.target_frame, text="Workshop Slot(s):").grid(row=4, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.workshop_slots_entry = ctk.CTkEntry(self.App.target_frame)
        self.workshop_slots_entry.insert(0, "1")  # Default value
        self.workshop_slots_entry.grid(row=4, column=1, padx=10, pady=5)  # Increased padding

        # heroes
        ctk.CTkLabel(self.App.target_frame, text="Heroes Slot(s):").grid(row=5, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.heroes_slots_entry = ctk.CTkEntry(self.App.target_frame)
        self.heroes_slots_entry.insert(0, "1")  # Default value
        self.heroes_slots_entry.grid(row=5, column=1, padx=10, pady=5)  # Increased padding

        # spell
        ctk.CTkLabel(self.App.target_frame, text="Spell Slot(s):").grid(row=6, column=0, padx=10, pady=5, sticky="w")  # Increased padding
        self.spell_slots_entry = ctk.CTkEntry(self.App.target_frame)
        self.spell_slots_entry.insert(0, "1")  # Default value
        self.spell_slots_entry.grid(row=6, column=1, padx=10, pady=5)  # Increased padding

    def toggle_gold_target(self):
        if self.gold_target_check.get():
            self.gold_target_entry.configure(state="normal")
        else:
            self.gold_target_entry.configure(state="disabled")

    def toggle_elixir_target(self):
        if self.elixir_target_check.get():
            self.elixir_target_entry.configure(state="normal")
        else:
            self.elixir_target_entry.configure(state="disabled")

    def toggle_dark_elixir_target(self):
        if self.dark_elixir_target_check.get():
            self.dark_elixir_target_entry.configure(state="normal")
        else:
            self.dark_elixir_target_entry.configure(state="disabled")

    def safe_int(self, entry, default=0):
        try:
            return int(entry.get())
        except ValueError:
            return default

    def log(self, message):
        textbox = self.App.log_textbox._textbox
        textbox.tag_configure("spacing", spacing3=8)
        textbox.insert("end", message + "\n", "spacing")
        textbox.see("end")

    def get_targets(self):
        return {
            "gold_target": self.safe_int(self.gold_target_entry),
            "elixir_target": self.safe_int(self.elixir_target_entry),
            "dark_elixir_target": self.safe_int(self.dark_elixir_target_entry),
            "gold_remaining": self.safe_int(self.gold_remaining_entry),
            "elixir_remaining": self.safe_int(self.elixir_remaining_entry),
            "dark_elixir_remaining": self.safe_int(self.dark_elixir_remaining_entry),
            "gold_target_enabled": self.gold_target_check.get(),
            "elixir_target_enabled": self.elixir_target_check.get(),
            "dark_elixir_target_enabled": self.dark_elixir_target_check.get(),
            "troop_slots": self.safe_int(self.troop_slots_entry),
            "workshop_slots": self.safe_int(self.workshop_slots_entry),
            "heroes_slots": self.safe_int(self.heroes_slots_entry),
            "spell_slots": self.safe_int(self.spell_slots_entry),
        }

    def run(self):
        self.App.mainloop()

cls_clash_of_clans_bot_app = ClasherControls()

# Instantiate and run the application
if __name__ == "__main__":
    app = cls_clash_of_clans_bot_app
    app.run()