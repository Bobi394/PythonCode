import tkinter as tk
from tkinter import ttk
import threading
import random
import time
from pynput.keyboard import Controller

# Initialisiere Keyboard-Controller
keyboard = Controller()

# Globale Variablen
running = False
next_jump_in = 0
start_time = None
thread = None

# Funktion für den Sprung
def jump():
    keyboard.press(' ')
    keyboard.release(' ')

# Hintergrundfunktion zum Steuern des Bots
def bot_loop(min_time, max_time):
    global running, next_jump_in, start_time

    # Fester erster Sprung nach 10s, zweiter nach 20s
    festen_spruenge = [10, 20]
    sprung_index = 0

    while running:
        if sprung_index < len(festen_spruenge):
            next_jump_in = festen_spruenge[sprung_index]
            sprung_index += 1
        else:
            next_jump_in = random.randint(min_time, max_time)

        start_time = time.time()

        while time.time() - start_time < next_jump_in and running:
            time.sleep(1)
            remaining = next_jump_in - int(time.time() - start_time)
            if remaining >= 0:
                countdown_var.set(f"Nächster Sprung in: {remaining}s")

        if running:
            jump()
            countdown_var.set("🕹️ Gesprungen!")

# Startet den Bot-Thread
def start_bot():
    global running, thread

    try:
        min_time = int(min_entry.get())
        max_time = int(max_entry.get())

        if min_time >= max_time:
            countdown_var.set("⚠️ Min < Max!")
            return
    except ValueError:
        countdown_var.set("⚠️ Ungültige Zahl!")
        return

    if not running:
        running = True
        thread = threading.Thread(target=bot_loop, args=(min_time, max_time), daemon=True)
        thread.start()
        countdown_var.set("Bot läuft...")

# Stoppt den Bot
def stop_bot():
    global running
    running = False
    countdown_var.set("⏹️ Bot gestoppt.")

# GUI erstellen
root = tk.Tk()
root.title("🌱 JumpBot von Skipi 🦎")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="⏱️ Min Zeit (s):").grid(column=0, row=0, sticky="w")
min_entry = ttk.Entry(frame)
min_entry.insert(0, "30")  # Standardwert
min_entry.grid(column=1, row=0)

ttk.Label(frame, text="⏱️ Max Zeit (s):").grid(column=0, row=1, sticky="w")
max_entry = ttk.Entry(frame)
max_entry.insert(0, "300")  # Standardwert
max_entry.grid(column=1, row=1)

ttk.Button(frame, text="▶️ Start", command=start_bot).grid(column=0, row=2, pady=10)
ttk.Button(frame, text="⏹️ Stop", command=stop_bot).grid(column=1, row=2, pady=10)

countdown_var = tk.StringVar()
countdown_label = ttk.Label(frame, textvariable=countdown_var, font=("Segoe UI", 12))
countdown_label.grid(column=0, row=3, columnspan=2)

root.mainloop()


