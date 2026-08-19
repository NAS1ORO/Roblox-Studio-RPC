# Roblox Studio Discord Rich Presence (CMD-Style)

A lightweight, standalone Python-based utility that displays your current development status in **Roblox Studio** directly on your Discord profile. It features an interactive command-line interface for configuration and supports seamless, invisible background execution on Windows startup.

## ⚡ Features

- 🛠 **CMD-Style CLI:** An interactive text menu to manage all app configurations instantly.
- 🚀 **Silent Autofun:** Registers the executable to the Windows Registry with a hidden flag (`--background`), executing with zero terminal windows shown on boot.
- 🖼 **Dynamic Place Assets:** Map specific Roblox Studio place names to custom image URLs on the fly.
- 🔄 **Hot-Reloading:** The background worker re-reads the local JSON configuration every 3 seconds—no manual restarts required when updates are made.

---

## 🔷 Installation & Compilation

Since a compiled `.exe` cannot overwrite its own binary contents, settings are stored externally in a local `config.json` generated alongside the app.

## 📥 Download

You can download the compiled standalone application from the official release page:
👉 **[Download Roblox Studio RPC v0.8.2](https://github.com/NAS1ORO/Roblox-Studio-RPC/releases/tag/0.8.2)**

### 🛑 Prerequisites
Make sure you have Python installed and the required dependencies fetched:
```bash
pip install pypresence pygetwindow
pip install pyinstaller
```

### ⚠️ Building the Executable
To package the tool into a clean standalone application with a custom icon, use the following compilation setup (replace `icon.ico` with your asset file name):

```bash
pyinstaller --clean --onefile --icon=icon.ico Module.py
```
*Note: Do not use the `--noconsole` modifier during PyInstaller packaging, as the built-in conditional wrapper handles silent boot routines securely through native Windows WinAPI methods.*

---

## 🚧 Configuration & Usage

Once built, move the compiled file from the `dist/` directory into your preferred working folder and run it.

### Menu Options
1. **Windows Startup:** Toggle the automated silent background run behavior on system startup (`y/n`).
2. **Configure place assets/images:** 
   - **Add image asset:** Input the exact Studio place name and pair it with a direct CDN asset link.
   - **Remove image asset:** View an indexed list of current rules and remove items by entering their sequence number.
3. **Start RPC immediately:** Initiates the Discord Presence wrapper directly within the active terminal workspace for testing or immediate use without system reboots.

---

## ℹ️ Project Structure
- `Module.py` — Core source file containing configuration interfaces and the Presence routing event loop.
- `config.json` — Generated database storing runtime keys, startup toggles, and customized dictionary rules.
