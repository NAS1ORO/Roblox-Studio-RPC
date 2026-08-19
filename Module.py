import os
import sys
import json
import time
import winreg
import ctypes
import pygetwindow as gw
from pypresence import Presence

CONFIG_FILE = "config.json"
REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "RobloxStudioRPC"

DEFAULT_CONFIG = {
    "CLIENT_ID": "1539562410644611122",
    "DEFAULT_IMAGE": "app",
    "AUTORUN": False,
    "PLACE_IMAGES": {
    }
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def set_autorun(status):
    exe_path = os.path.abspath(sys.argv[0])
    cmd = f'"{exe_path}" --background'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE)
        if status:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Registry modification error: {e}")
        return False

def hide_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

def run_rpc_background():
    config = load_config()
    CLIENT_ID = config.get("CLIENT_ID", "1539562410644611122")
    DEFAULT_IMAGE = config.get("DEFAULT_IMAGE", "app")
    
    RPC = Presence(CLIENT_ID)
    rpc_connected = False

    try:
        RPC.connect()
        rpc_connected = True
    except:
        pass

    last_title = ""
    start_time = None

    while True:
        config = load_config()
        PLACE_IMAGES = config.get("PLACE_IMAGES", {})

        if not rpc_connected:
            try:
                RPC.connect()
                rpc_connected = True
            except:
                time.sleep(5)
                continue

        studio_windows = [w for w in gw.getAllWindows() if "Roblox Studio" in w.title]
        
        if studio_windows:
            window = studio_windows[0]
            full_title = window.title
            
            if full_title != last_title:
                last_title = full_title
                start_time = time.time()
                
                place_name = full_title.replace(" - Roblox Studio", "").strip()
                
                if place_name == "" or place_name == "Roblox Studio":
                    place_name = "Main menu"
                    state = "In menu"
                    large_image = DEFAULT_IMAGE
                else:
                    state = "Edit place"
                    if place_name in PLACE_IMAGES:
                        large_image = PLACE_IMAGES[place_name]
                    else:
                        large_image = DEFAULT_IMAGE
                
                try:
                    RPC.update(
                        details=f"{place_name}",
                        state=state,
                        large_image=large_image,
                        large_text=place_name,
                        start=start_time
                    )
                except:
                    pass
        else:
            if last_title != "":
                try:
                    RPC.clear()
                except:
                    pass
                last_title = ""
                start_time = None

        time.sleep(3)

def run_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        config = load_config()
        
        print("="*40)
        print("  ROBLOX STUDIO RPC - SETTINGS")
        print("="*40)
        autorun_status = "ENABLED" if config.get("AUTORUN", False) else "DISABLED"
        print(f"1. Windows Startup (Silent background run): [{autorun_status}]")
        print("2. Configure place assets/images")
        print("3. Start RPC immediately (in this window)")
        print("0. Exit")
        print("="*40)
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            ans = input("Enable hidden background startup on Windows boot? (y/n): ").strip().lower()
            if ans == 'y':
                if set_autorun(True):
                    config["AUTORUN"] = True
                    save_config(config)
                    print("[+] Startup successfully enabled!")
            elif ans == 'n':
                if set_autorun(False):
                    config["AUTORUN"] = False
                    save_config(config)
                    print("[-] Startup disabled.")
            else:
                print("Invalid input.")
            time.sleep(1.5)
            
        elif choice == "2":
            run_images_menu()
            
        elif choice == "3":
            print("\nStarting RPC... Close this terminal window to stop.")
            run_rpc_background()
            
        elif choice == "0":
            break

def run_images_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        config = load_config()
        images = config.get("PLACE_IMAGES", {})
        
        print("="*40)
        print("  ASSET IMAGE CONFIGURATION")
        print("="*40)
        print("1. Add image asset")
        print("2. Remove image asset")
        print("0. Back")
        print("="*40)
        
        choice = input("Select an action: ").strip()
        
        if choice == "1":
            place_name = input("Enter exact place name (as seen in Studio): ").strip()
            if not place_name: continue
            img_url = input("Enter direct image link/key: ").strip()
            if not img_url: continue
            
            images[place_name] = img_url
            config["PLACE_IMAGES"] = images
            save_config(config)
            print("[+] Asset added and saved successfully!")
            time.sleep(1.5)
            
        elif choice == "2":
            if not images:
                print("The asset list is completely empty.")
                time.sleep(1.5)
                continue
                
            print("\nList of configured places:")
            img_list = list(images.keys())
            for idx, name in enumerate(img_list, 1):
                print(f"{idx}. {name} -> {images[name][:40]}...")
                
            try:
                num = int(input("\nEnter the index number to delete: ").strip())
                if 1 <= num <= len(img_list):
                    target_name = img_list[num - 1]
                    confirm = input(f"Are you sure you want to delete '{target_name}'? (y/n): ").strip().lower()
                    if confirm == 'y':
                        del images[target_name]
                        config["PLACE_IMAGES"] = images
                        save_config(config)
                        print("[+] Successfully deleted.")
                    else:
                        print("Operation canceled.")
                else:
                    print("Index out of bounds.")
            except ValueError:
                print("Please enter a valid numeric value.")
            time.sleep(1.5)
            
        elif choice == "0":
            break

if __name__ == "__main__":
    if "--background" in sys.argv:
        hide_console()
        run_rpc_background()
    else:
        run_menu()
