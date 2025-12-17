# 安裝與設定指南

## 系統要求

- Python 3.8 以上
- pip（Python 套件管理工具）
- 現代化網頁瀏覽器（Chrome、Firefox、Safari、Edge）

## 快速開始

### 1. 取得專案

```bash
git clone <repository-url>
cd skills_copilot-integrate-mcp
```

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 3. 執行應用程式

```bash
cd src
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

伺服器將在 `http://localhost:8000` 啟動。

### 4. 訪問應用程式

在網頁瀏覽器中開啟 `http://localhost:8000`，即可看到 Mergington 高中活動管理介面。

## 開發容器設定

本專案包含 Dev Container 配置，允許在隔離的容器環境中開發：

1. 安裝 [VS Code Remote Containers 延伸](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. 開啟專案資料夾
3. 使用命令 `Remote-Containers: Reopen in Container` 在容器內開啟專案

## 依賴套件

詳見 [requirements.txt](../requirements.txt)：

- **FastAPI**：現代化 Python 網頁框架
- **Uvicorn**：ASGI 伺服器

## 環境變數

目前應用程式無需設置環境變數。所有設定使用預設值。

## 故障排除

### 埠口 8000 已佔用

若遇到「埠口已在使用」的錯誤，可改用其他埠口：

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

### 模組未找到錯誤

確認已執行 `pip install -r requirements.txt` 並正確安裝所有依賴。

### 無法連線到伺服器

確認伺服器已啟動，且瀏覽器使用正確的網址（預設為 `http://localhost:8000`）。
