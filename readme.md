# Clash of Clans Bot (CoC Bot)

## Features

- **Customisable Attacks:**  
  Easily switch between different attack strategies (Super Drag, Pekka spam, Builder Base, etc.) by editing the attack type or using the GUI. Attack logic is modular and can be extended in `attacks.py`.

- **Builder Base Compatibility:**  
  Includes a dedicated Builder Base bot (`builderbot.py`) for automating attacks in the Builder Base. The bot  executes attacks, and returns home automatically.

- **Autonomous Loot Farm:**  
  The main bot (`main.py`) automatically searches for bases with high loot, attacks them, and repeats the process. It uses OCR to read loot values and only attacks when thresholds are met.

## How to Use

1. **Install Requirements:**  
   - Python 3
   - Install required Python libraries: `pip install -r requirements.txt`

2. **Configure Emulator:**  
   - Ensure Android emulator is running and accessible via ADB (`platform-tools`).
   - Set the ADB port in the `attacks.py` file.

3. **Run the Bot:**  
   - For main base farming:  
     `python main.py`

4. **Customise Attacks:**  
   - Edit `attacktype` in `Bot.py` or add new strategies in `attacks.py`.

5. **Dynamic Target Configuration:**  
   - Use the GUI to dynamically set loot targets, troop slots, hero slots, and spell slots.  
   - Enable or disable specific loot targets (Gold, Elixir, Dark Elixir) directly from the GUI.

## Files

- `main.py` — Main loot farming bot with GUI.
- `attacks.py` — Contains all attack strategies.
- `func.py` — Utility functions for screen interaction and OCR.

## Disclaimer

This bot is for educational purposes only. Use at your own risk.  
Automating gameplay may violate Clash of Clans' Terms of Service.
