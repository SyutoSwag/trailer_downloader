# Trailer Downloader Script

這個 Python 腳本會從指定網站 (`https://javtrailers.com`) 抓取所有包含 `video` 的連結，提取 M3U8 播放列表的 URL 和影片標題，並使用 `ffmpeg` 下載影片，將其保存到 `output` 文件夾中。

## 前置作業

在運行這個腳本之前，請確保你的系統已經安裝了以下工具和庫：

### 1. 安裝 Python

請確保你的系統已安裝 Python。如果沒有，請從 [Python 官方網站](https://www.python.org/downloads/) 下載並安裝最新版本的 Python。

### 2. 安裝 `pip`

`pip` 是 Python 的包管理工具，用於安裝和管理 Python 庫。如果你還沒有安裝 `pip`，可以按照以下步驟安裝：

1. 下載 `get-pip.py` 文件：
   ```sh
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   ```
2. 運行 `get-pip.py` 來安裝 `pip`：
   ```sh
   python get-pip.py
   ```
   
### 3. 安裝所需的 Python 庫

使用 `pip` 安裝腳本所需的庫：
```sh
pip install requests beautifulsoup4
```

### 4. 安裝 ffmpeg

ffmpeg 是一個多媒體處理工具，用於下載和處理多媒體文件。請按照以下步驟安裝 ffmpeg：

#### 在 macOS 上安裝 ffmpeg

1. 安裝 Homebrew（如果尚未安裝）：

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. 使用 Homebrew 安裝 ffmpeg：

```sh
brew install ffmpeg
```

#### 在 Windows 上安裝 ffmpeg

1. 從 ffmpeg [官方網站](https://ffmpeg.org/download.html) 下載適用於 Windows 的版本。
2. 解壓縮下載的文件到一個目錄（例如 C:\ffmpeg）。
3. 將 ffmpeg 的 bin 目錄添加到系統的 PATH 環境變數中。

## 運行腳本

按照以下步驟運行腳本：

1. `下載 trailer_downloader.py`。
2. 在終端（Terminal）或命令提示符（Command Prompt）中導航到檔案所在的目錄。
3. 運行腳本：
```sh
python trailer_downloader.py
```
