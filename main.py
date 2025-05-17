import pytesseract
from PIL import Image, ImageFilter, ImageOps
import pyautogui
import time
import tkinter as tk
from googletrans import Translator

# 设置 tesseract 路径（根据你的安装路径）
pytesseract.pytesseract.tesseract_cmd = r'E:\OCR\tesseract.exe'

# 初始截取区域
region = [100, 100, 1280, 800]  # [left, top, width, height]

translator = Translator()

def update_text():
    screenshot = pyautogui.screenshot(region=tuple(region))
    # 转为灰度
    img = screenshot.convert('L')
    # 自适应二值化
    img = ImageOps.autocontrast(img)
    img = img.point(lambda x: 0 if x < 160 else 255, '1')
    # 可选：锐化
    img = img.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(img, lang='jpn')
    try:
        translated = translator.translate(text, src='ja', dest='zh-cn').text
    except Exception as e:
        translated = f"翻译出错: {e}"
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, f"原文：\n{text}\n\n译文:\n{translated}")
    root.after(1000, update_text)  # 每秒更新一次

def move_start(event):
    box._drag_data = (event.x_root, event.y_root, region[0], region[1])

def move_drag(event):
    dx = event.x_root - box._drag_data[0]
    dy = event.y_root - box._drag_data[1]
    region[0] = box._drag_data[2] + dx
    region[1] = box._drag_data[3] + dy
    box.geometry(f"{region[2]}x{region[3]}+{region[0]}+{region[1]}")

def resize_start(event):
    box._resize_data = (event.x_root, event.y_root, region[2], region[3])

def resize_drag(event):
    dx = event.x_root - box._resize_data[0]
    dy = event.y_root - box._resize_data[1]
    new_w = max(50, box._resize_data[2] + dx)
    new_h = max(30, box._resize_data[3] + dy)
    region[2] = new_w
    region[3] = new_h
    box.geometry(f"{region[2]}x{region[3]}+{region[0]}+{region[1]}")
    canvas.config(width=region[2], height=region[3])
    canvas.delete("all")
    canvas.create_rectangle(2, 2, region[2]-2, region[3]-2, outline='red', width=4)
    # 右下角小方块用于缩放
    canvas.create_rectangle(region[2]-16, region[3]-16, region[2]-2, region[3]-2, fill='red', outline='red')

root = tk.Tk()
root.title("实时日文识别输出")

# 添加滚动条
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 设置自动换行和绑定滚动条
text_widget = tk.Text(root, width=50, height=15, font=("Consolas", 14), wrap=tk.WORD, yscrollcommand=scrollbar.set)
text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_widget.yview)

# 创建红色方框窗口
box = tk.Toplevel(root)
box.overrideredirect(True)
box.attributes('-topmost', True)
box.attributes('-alpha', 0.3)

box.geometry(f"{region[2]}x{region[3]}+{region[0]}+{region[1]}")

canvas = tk.Canvas(box, width=region[2], height=region[3], highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_rectangle(2, 2, region[2]-2, region[3]-2, outline='red', width=4)
canvas.create_rectangle(region[2]-16, region[3]-16, region[2]-2, region[3]-2, fill='red', outline='red')

# 绑定拖动事件（左键拖动移动窗口）
canvas.bind("<ButtonPress-1>", move_start)
canvas.bind("<B1-Motion>", move_drag)
def resize_check(event):
    # 判断是否在右下角小方块区域
    if region[2]-16 <= event.x <= region[2] and region[3]-16 <= event.y <= region[3]:
        canvas.bind("<B1-Motion>", resize_drag)
        canvas.bind("<ButtonRelease-1>", lambda e: canvas.bind("<B1-Motion>", move_drag))
    else:
        canvas.bind("<B1-Motion>", move_drag)
canvas.bind("<ButtonPress-1>", resize_check, add='+')
canvas.bind("<ButtonPress-3>", move_start)

# 标志变量，记录当前是否在缩放
is_resizing = {'flag': False}

def mouse_down(event):
    # 判断是否在右下角小方块
    if region[2]-16 <= event.x <= region[2] and region[3]-16 <= event.y <= region[3]:
        is_resizing['flag'] = True
        resize_start(event)
    else:
        is_resizing['flag'] = False
        move_start(event)

def mouse_move(event):
    if is_resizing['flag']:
        resize_drag(event)
    else:
        move_drag(event)

canvas.bind("<ButtonPress-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)

update_text()
root.mainloop()
