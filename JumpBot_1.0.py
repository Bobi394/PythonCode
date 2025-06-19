import time
import random
import requests
from bs4 import BeautifulSoup
from pynput.keyboard import Controller
from datetime import datetime
import threading

# 🔗 Webseite & HTML-ID
URL = "https://ff130j.mimo.run/index.html"
CHECK_ID = "JumpBot_1.0"
keyboard = Controller()

# Bot-Zustände
bot_aktiviert = False
stop_event = threading.Event()

# Webseite prüfen
def lese_status():
    try:
        r = requests.get(URL, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        elem = soup.find(id=CHECK_ID)
        if elem:
            return elem.text.strip().lower()
        else:
            return "fehler"
    except Exception as e:
        print(f"⚠️ Fehler beim Webseiten-Check: {e}")
        return "fehler"

# Bot-Sprung-Thread
def springe_bot():
    while not stop_event.is_set():
        wait = random.randint(20, 180)
        print(f"⏳ Warte {wait} Sekunden...")
        for _ in range(wait):
            if stop_event.is_set():
                return
            time.sleep(1)

        now = datetime.now().strftime("%H:%M:%S")
        keyboard.press(' ')
        time.sleep(0.1)
        keyboard.release(' ')
        print(f"⬆️ [{now}] Leertaste gedrückt!")

# Hauptprogramm
print("🦎 Skipi-Bot gestartet – wartet auf Aktivierung...")

bot_thread = None

try:
    while True:
        status = lese_status()

        if status == "true" and not bot_aktiviert:
            print("✅ Bot wurde AKTIVIERT!")
            bot_aktiviert = True
            stop_event.clear()
            bot_thread = threading.Thread(target=springe_bot)
            bot_thread.start()

        elif status == "false" and bot_aktiviert:
            print("🛑 Bot wurde gestoppt!")
            stop_event.set()
            bot_thread.join()
            bot_aktiviert = False

        elif status == "update":
            if bot_aktiviert:
                print("🛑 Bot wird gestoppt wegen Update-Hinweis.")
                stop_event.set()
                bot_thread.join()
                bot_aktiviert = False
            print("⚠️ Bitte update deine Version! (Skipi-Bot ❌ alt)")

        time.sleep(1)

except KeyboardInterrupt:
    print("\n❌ Skipi-Bot komplett gestoppt.")
    stop_event.set()
    if bot_thread:
        bot_thread.join()
