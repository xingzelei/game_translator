# Game Translator（日文游戏实时翻译工具）

## 简介

本项目是一个基于 OCR（光学字符识别）和 Google 翻译的日文游戏实时翻译工具。  
它可以实时截取屏幕指定区域的内容，自动识别日文文本并翻译为中文，适合游戏、漫画等场景下的辅助理解。

## 功能特色

- 实时截屏指定区域，自动识别日文文本
- 自动调用 Google 翻译，将日文翻译为中文
- 支持鼠标拖动和缩放红色方框，灵活调整识别区域
- 识别结果自动换行并支持滚动查看
- 适用于色彩丰富、复杂背景的图片

## 使用方法

### 1. 安装依赖

请先安装以下 Python 库：

```sh
pip install pillow pyautogui pytesseract googletrans==4.0.0-rc1
```

并确保已安装 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)  
安装后将 `tesseract.exe` 路径配置到代码中的 `pytesseract.pytesseract.tesseract_cmd`。

### 2. 运行程序

直接运行 `main.py`：

```sh
python main.py
```

### 3. 操作说明

- 程序启动后，会弹出一个主窗口显示识别和翻译结果。
- 屏幕上会出现一个红色半透明方框，表示当前的识别区域。
- **拖动红框**：按住红框任意位置拖动，可移动识别区域。
- **缩放红框**：按住红框右下角的小红块拖动，可调整识别区域大小。
- 识别和翻译结果会自动刷新显示在主窗口中。

## 常见问题

- **识别不准？**  
  可尝试调整识别区域大小、位置，或修改二值化阈值（`lambda x: 0 if x < 160 else 255`）。
- **翻译失败？**  
  可能是网络问题或 Google 翻译接口被限制，可稍后重试。
- **Tesseract 报错？**  
  请确认已正确安装 Tesseract，并配置了正确的路径，且已安装日文语言包（`jpn.traineddata`）。

## 依赖环境

- Python 3.7+
- pillow
- pyautogui
- pytesseract
- googletrans==4.0.0-rc1
- Tesseract OCR（需安装日文语言包）

## 许可证

MIT License

---

如有问题欢迎反馈！