# Clash of Clans Bot (CoC Bot)

## Features

- **Customisable Attacks:**  
  Easily switch between different attack strategies (Super Drag, Pekka spam, Builder Base, etc.) by editing the attack type or using the GUI. Attack logic is modular and can be extended in `attacks.py`.

- **Builder Base Compatibility:**  
  Includes a dedicated Builder Base bot (`builderbot.py`) for automating attacks in the Builder Base. The bot  executes attacks, and returns home automatically.

- **Autonomous Loot Farm:**  
  The main bot (`Bot.py`) automatically searches for bases with high loot, attacks them, and repeats the process. It uses OCR to read loot values and only attacks when thresholds are met.

- **Fake Legends League Option:**  
  stays within set trophie range (4930-4970) so you get legends leuge bonus while having unlimited attacks.

## How to Use

1. **Install Requirements:**  
   - Python 3

2. **Configure Emulator:**  
   - Ensure Android emulator is running and accessible via ADB (`platform-tools`).
   - set adb port in the `attacks.py` file

3. **Run the Bot:**  
   - For main base farming:  
     `python Bot.py`
   - For Builder Base farming:  
     `python builderbot.py`

4. **Customise Attacks:**  
   - Edit `attacktype` in `Bot.py` or add new strategies in `attacks.py`.

5. **Fake Legends League:**  
   - Set `trophiebypass = False` in `Bot.py` to enable.

## Files

- `Bot.py` — Main loot farming bot with GUI.
- `builderbot.py` — Builder Base attack automation bot.
- `attacks.py` — Contains all attack strategies.
- `func.py` — Utility functions for screen interaction and OCR.

## Disclaimer

This bot is for educational purposes only. Use at your own risk.  
Automating gameplay may violate Clash of Clans' Terms of Service.
