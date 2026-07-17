# win-background-clicker
A lightweight, high-precision Python utility designed to send background mouse clicks to specific application windows or child controls using the Windows (Win32) API. 

Unlike traditional macro recorders or auto-clickers that hijack your cursor, `win-background-clicker` locks onto the target window's process handle (`HWND`). This allows it to simulate mouse events digitally behind the scenes—keeping your physical mouse **100% free** so you can continue working, typing, or browsing uninterrupted.

---

## 🚀 Key Features

* **True Background Click (Non-Intrusive):** Uses low-level Windows message queues (`PostMessage`) to click targets without moving your physical mouse pointer.
* **Precise Timestamp Engine:** Eliminates "Time Drift" accumulative delays by utilizing system clock loops instead of standard `time.sleep()` blocks.
* **Low-Level Global Hotkeys:** Powered by Windows Kernel Hooks to ensure responsive controls (`p` to Pause/Resume, `q` to Quit) even under heavy multi-tasking.
* **Smart Auto-Buffer:** Built-in configurable safety buffer to perfectly align with application rendering cycles (e.g., waiting for replay buttons to pop up).
* **Universal Capability:** Works seamlessly with Android Emulators (LDPlayer, Nox, BlueStacks), Web Browsers (Chrome, Edge), and standard media players.

---

## 🛠️ Architecture & How It Works

1. **Window Target Locking:** When you press `p`, the script captures the specific Child Window Handle (`HWND`) directly under your cursor via `win32gui.WindowFromPoint`.
2. **Coordinate Mapping:** It translates the absolute Screen Coordinates to internal Window Client Coordinates using `win32gui.ScreenToClient`.
3. **Digital Signaling:** The automation loop pushes digital signals (`WM_LBUTTONDOWN` & `WM_LBUTTONUP`) directly into the target application’s message queue without interfering with the OS hardware layer.

---

## 📋 Prerequisites

This script requires Windows OS and Python 3.x. Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```
Or install them manually:

```Bash
pip install keyboard pywin32 pynput
```

## 🎮 How to Use
1. Run the script via terminal:

```Bash
python autoclick.py
```

2. Enter your desired loop delay (Minutes and Seconds) based on your video length or target interval.

3. Hover your physical mouse pointer over the target button (e.g., the video replay button inside LDPlayer or Chrome).

4. Press p to lock the target window and activate the bot. The bot will perform an immediate initial click and run silently in the background.

5. You can now move your mouse away and use your computer normally!

6. Press p again to Pause/Resume the loop, or press q to Exit and terminate all threads safely.

## 📂 Project Structure
win-background-clicker/
├── autoclick.py          # Main execution script
├── requirements.txt      # Dependency list
├── .gitignore            # Standard Python environment filter
└── README.md             # Documentation

## ⚖️ License & Disclaimer
This project is for educational and personal utility purposes. Use responsibly when automating clicks on production environments or third-party platforms.