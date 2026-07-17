import time
import threading
import sys
import keyboard
import win32gui
import win32con
from pynput.mouse import Controller as MouseController

# --- Input Delay Time ---
print("=== Target Specific Background Clicker ===")
minutes = int(input("Enter minutes (0 if none): "))
seconds = int(input("Enter seconds (0 if none): "))

BUFFER_TIME = 2 
BASE_DELAY = (minutes * 60) + seconds
DELAY = BASE_DELAY + BUFFER_TIME

print(f"[SETTING] Video length: {BASE_DELAY}s | Buffer added: {BUFFER_TIME}s")
print(f"[SETTING] Total loop cycle: {DELAY} seconds\n")

mouse = MouseController()
running = False
next_click_time = 0

# ตัวแปรสำหรับล็อกเป้าหมายเบื้องหลัง
hwnd_target = None
relative_x = 0
relative_y = 0

def make_lparam(x, y):
    return (y << 16) | (x & 0xFFFF)

def send_background_click():
    """ส่งคำสั่งคลิกซ้ายไปที่หน้าต่างย่อยภายในโดยตรง"""
    global hwnd_target
    if hwnd_target:
        try:
            lParam = make_lparam(relative_x, relative_y)
            
            # ส่ง Click Down และ Up ไปยังจุดโฟกัสย่อยภายใน
            win32gui.PostMessage(hwnd_target, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(0.01)
            win32gui.PostMessage(hwnd_target, win32con.WM_LBUTTONUP, 0, lParam)
            print(f"[INFO] Background click sent to Target HWND: {hwnd_target} at ({relative_x}, {relative_y})")
        except Exception as e:
            print(f"[ERROR] Failed to send click: {e}")

def clicker_loop():
    global running, next_click_time
    while True:
        if running and hwnd_target:
            current_time = time.time()
            if current_time >= next_click_time:
                send_background_click()
                next_click_time = time.time() + DELAY
        time.sleep(0.05)

def toggle_bot():
    """ฟังก์ชันเมื่อกดปุ่ม P"""
    global running, next_click_time, hwnd_target, relative_x, relative_y
    running = not running
    if running:
        # บันทึกพิกัดและหน้าต่างย่อย (Child Window) ณ จุดที่เมาส์ชี้อยู่โดยตรง (ไม่แปลงเป็นตัวแม่)
        x, y = mouse.position
        hwnd_target = win32gui.WindowFromPoint((x, y)) 
        
        # แปลงพิกัดจอให้เป็นพิกัดภายในหน้าต่างย่อยตัวนี้
        relative_x, relative_y = win32gui.ScreenToClient(hwnd_target, (x, y))
        
        print(f"\n[STATUS] Bot Started [ON]")
        print(f"[TARGET] Specific HWND: {hwnd_target} | Internal Coords: ({relative_x}, {relative_y})")
        
        # คลิกทันทีก่อน 1 ครั้ง
        send_background_click()
        next_click_time = time.time() + DELAY
    else:
        print("\n[STATUS] Bot Paused [OFF]")

def quit_bot():
    print("\n[EXIT] Program closed completely.")
    sys.exit()

# ลงทะเบียน Hotkeys
keyboard.add_hotkey('p', toggle_bot)
keyboard.add_hotkey('q', quit_bot)

# รัน Thread หลังบ้านสำหรับตัวคลิก
click_thread = threading.Thread(target=clicker_loop, daemon=True)
click_thread.start()

print(f"=== Program Ready ===")
print(f"-> Hover your mouse over the video replay button inside LDPlayer and press 'p'")
print(f"-> Press 'p' again to Pause / Press 'q' to Close the program.")
print("=====================\n")

keyboard.wait()