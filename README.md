# Game Translator

一个基于 OCR 和机器翻译的实时日文文本识别与翻译工具，支持自定义截图区域，适合游戏等场景下的日文文本实时翻译。

## 功能简介

- 实时截取屏幕指定区域，自动识别日文文本并翻译为中文
- 支持拖动和缩放截图区域
- 采用多线程，界面流畅不卡顿
- 支持彩色图片的文字提取（自动进行图像增强处理以提升识别率）

## 依赖环境

- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)（需安装并配置路径）
- pip 包：
  - pytesseract
  - pillow
  - pyautogui
  - googletrans
  - tkinter（标准库自带）

## 安装方法

1. 安装 Tesseract，并记下安装路径（如 `E:\OCR\tesseract.exe`）。
2. 安装 Python 依赖：
   ```bash
   pip install pytesseract pillow pyautogui googletrans==4.0.0-rc1
   ```

## 使用方法

1. 修改 `main.py` 中的 tesseract 路径为你的实际安装路径：
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'E:\OCR\tesseract.exe'
   ```
2. 运行程序：
   ```bash
   python main.py
   ```
3. 拖动红色方框调整识别区域，右下角小红块可缩放区域。
4. 程序会自动识别区域内的日文并翻译为中文，显示在主窗口。

## 主要代码逻辑

- 使用 `pyautogui.screenshot` 截取指定区域
- 图像自动灰度、增强、二值化、锐化，提高 OCR 识别率
- 用 `pytesseract` 识别日文文本
- 用 `googletrans` 翻译为中文
- 所有耗时操作均在后台线程执行，界面不卡顿

## 注意事项

- 若遇到窗口卡顿或无响应，请确保已安装所有依赖，并用管理员权限运行。
- 若翻译失败，可能是网络问题或 Google 翻译接口限制。



如有问题欢迎反馈！