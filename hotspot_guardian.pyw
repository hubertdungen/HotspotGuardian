import subprocess
import time
import sys
import win32gui
import win32con
import pystray
from PIL import Image
import threading
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

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
        subprocess.run(["powershell", "-Command", "Add-Type -AssemblyName System.Runtime.WindowsRuntime; $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]; $asTask = $asTaskGeneric.MakeGenericMethod([Windows.Networking.Connectivity.NetworkOperationResult]); $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile(); $tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]::CreateFromConnectionProfile($connectionProfile); $asyncOperation = $tetheringManager.StartTetheringAsync(); $asTask.Invoke($null, @($asyncOperation)) | Wait-Task;"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_enable_hotspot():
    if not is_hotspot_on():
        turn_on_hotspot()

def run_periodic_check():
    while True:
        check_and_enable_hotspot()
        time.sleep(3600)  # Sleep for 1 hour

def on_quit(icon, item):
    icon.stop()
    sys.exit()

def create_image():
    image = Image.new('RGB', (64, 64), color='red')
    return image

def run():
    image = create_image()
    menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
    icon = pystray.Icon("hotspot_manager", image, "Hotspot Manager", menu)
    
    threading.Thread(target=run_periodic_check, daemon=True).start()
    
    icon.run()

if __name__ == "__main__":
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, win32con.SW_HIDE)
    
    run()