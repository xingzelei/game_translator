# 实时游戏文本识别与翻译工具

这是一个使用 Python 开发的实时屏幕文本识别与翻译工具，主要用于识别屏幕指定区域内的日文文本，并将其翻译成中文。

## 功能

*   **屏幕区域选择**：可以通过一个可拖动和调整大小的红色半透明方框来选择需要识别的屏幕区域。
*   **实时文本识别**：使用 EasyOCR 对选定区域内的图像进行光学字符识别 (OCR)，支持日文和英文。
*   **GPU 加速**：支持使用 GPU 进行 OCR，以提高识别速度（需要正确配置 CUDA 和 cuDNN）。
*   **实时翻译**：使用 Google Translate API 将识别出的日文文本翻译成中文。
*   **图形用户界面 (GUI)**：使用 Tkinter 创建一个简单的窗口，用于显示原文和译文。

## 技术栈

*   **Python 3**
*   **EasyOCR**: 用于文本识别。
*   **Pillow (PIL)**: 用于图像处理。
*   **PyAutoGUI**: 用于屏幕截图。
*   **Tkinter**: 用于创建图形用户界面。
*   **googletrans**: 用于文本翻译。
*   **NumPy**: EasyOCR 的依赖库。

## 安装

1.  **克隆或下载项目**
2.  **安装依赖库**:
    在项目根目录下打开终端，运行以下命令：
    ```bash
    pip install easyocr Pillow pyautogui googletrans==4.0.0rc1 numpy
    ```
    如果你希望使用 GPU 进行 OCR (推荐)，请确保你已安装 NVIDIA 驱动、CUDA Toolkit 和 cuDNN，并且安装了支持 GPU 的 PyTorch 版本。你可以访问 [PyTorch 官网](https://pytorch.org/get-started/locally/) 获取安装命令。

3.  **EasyOCR 模型下载**:
    首次运行脚本时，EasyOCR 会自动下载所需的模型文件。根据脚本中的设置，模型文件会下载到脚本所在目录下的 `.EasyOCR` 文件夹中。

## 使用方法

1.  运行 `main.py` 脚本：
    ```bash
    python main.py
    ```
2.  程序启动后，会出现两个窗口：
    *   一个主窗口，用于显示识别到的原文和翻译后的译文。
    *   一个红色的半透明方框，这是截图区域。
3.  **调整截图区域**：
    *   **移动**：鼠标左键按住红色方框内部并拖动。
    *   **调整大小**：鼠标左键按住红色方框右下角的小红块并拖动。
4.  程序会自动定时截取红色方框内的图像，进行文字识别和翻译，并在主窗口中更新结果。

## 注意事项

*   翻译功能依赖于 `googletrans` 库，可能会受到网络连接和 Google Translate API 政策的影响。
*   GPU 加速需要正确的环境配置。如果 GPU 不可用或配置不当，EasyOCR 会自动回退到 CPU 模式。
*   识别的准确性取决于图像质量、字体、背景复杂度等因素。

## 文件结构

```
game_translator/
│
├── main.py         # 主程序脚本
├── .EasyOCR/       # EasyOCR 模型文件存储目录 (首次运行后自动创建)
└── README.md       # 本说明文件
```