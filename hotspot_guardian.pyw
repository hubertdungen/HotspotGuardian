import subprocess
import time
import sys
import win32gui
import win32con
import pystray
from PIL import Image
import threading
import winreg
import json
import os
import ctypes
from tkinter import simpledialog, Tk

CONFIG_FILE = 'hotspot_guardian_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'check_interval': 3600}  # Default to 1 hour

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

def is_hotspot_on():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\icssvc\Settings")
        value, _ = winreg.QueryValueEx(key, "PeerlessState")
        winreg.CloseKey(key)
        return value == 1
    except WindowsError:
        return False

def turn_on_hotspot():
    try:
        # Using a simpler command to start the hotspot
        subprocess.run(["powershell", "-Command", "Start-Process -FilePath 'powershell.exe' -ArgumentList 'Start-NetConnectionProfile' -Verb runAs"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_enable_hotspot():
    if not is_hotspot_on():
        turn_on_hotspot()

def run_periodic_check():
    while True:
        check_and_enable_hotspot()
        time.sleep(config['check_interval'])

def on_quit(icon, item):
    icon.stop()
    sys.exit()

def set_check_interval(icon, item):
    global config
    root = Tk()
    root.withdraw()  # Hide the main window
    new_interval = simpledialog.askinteger("Set Check Interval", "Enter new check interval in seconds:", 
                                           minvalue=1, maxvalue=86400)  # 1 day max
    if new_interval:
        config['check_interval'] = new_interval
        save_config(config)
        print(f"Check interval updated to {new_interval} seconds")

def create_image():
    image = Image.new('RGB', (64, 64), color='red')
    return image

def run():
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("Set Check Interval", set_check_interval),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("hotspot_manager", image, "Hotspot Manager", menu)
    
    threading.Thread(target=run_periodic_check, daemon=True).start()
    
    icon.run()

if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    run()
