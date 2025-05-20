import os
import easyocr  # 引入 EasyOCR
from PIL import Image, ImageOps
import pyautogui
import tkinter as tk
from googletrans import Translator
import threading
import numpy as np

# 设置 EasyOCR 模型存储路径为当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['EASYOCR_MODULE_PATH'] = os.path.join(current_dir, '.EasyOCR')
# 初始截取区域
region = [100, 100, 1280, 800]  # [left, top, width, height]

translator = Translator()

# 初始化 EasyOCR Reader（支持日文和英文），并启用 GPU
reader = easyocr.Reader(['ja', 'en'], gpu=True)

def preprocess_image(img):
    # 转为灰度图（EasyOCR 不需要严格的二值化）
    img = img.convert('L')
    # 自适应增强对比度
    img = ImageOps.autocontrast(img)
    return img

def update_text_async():
    def task():
        screenshot = pyautogui.screenshot(region=tuple(region))
        img = preprocess_image(screenshot)
        # 转换为 NumPy 数组（EasyOCR 需要 NumPy 格式的图像）
        img_np = np.array(img)
        # 使用 EasyOCR 进行文字识别
        results = reader.readtext(img_np, detail=0)  # `detail=0` 只返回文字内容
        text = '\n'.join(results)  # 将识别结果拼接为字符串
        try:
            translated = translator.translate(text, src='ja', dest='zh-cn').text
        except Exception as e:
            translated = f"翻译出错: {e}"
        def update_ui():
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"原文：\n{text}\n\n译文:\n{translated}")
        root.after(0, update_ui)
        # 继续定时
        root.after(1000, update_text_async)
    threading.Thread(target=task, daemon=True).start()

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

update_text_async()
root.mainloop()
