# Prompt 輸出記錄

此檔案記錄所有由 GitHub Copilot 產出的主要文本成果，以建立可追溯的輸出日誌。

---

### 2025-12-17T00:00:00+08:00

- **Scope**: CHANGELOG.md, docs/installation.md, docs/configuration.md, docs/api.md, docs/Prompt-Output.md
- **Prompt**: 依規範建立文件
- **Output**:

  根據 `.github/instructions/update-docs-on-code-change.instructions.md` 規範，建立了以下文件：

  1. **CHANGELOG.md** - 版本歷史與變更日誌
     - 遵循 Keep a Changelog 與語意化版本規範
     - 包含 Added/Changed/Fixed/Deprecated/Removed/Security 等分類
     - 記錄專案初始設置與功能

  2. **docs/installation.md** - 安裝與設定指南
     - 系統要求與快速開始步驟
     - Dev Container 設定說明
     - 依賴套件說明
     - 故障排除指南

  3. **docs/configuration.md** - 設定指南
     - 伺服器設定（主機、埠口、熱重載）
     - 活動資料與資料持久性說明
     - CORS、日誌、最大參與者數限制說明

  4. **docs/api.md** - API 參考文件
     - 基礎資訊與 API 端點完整說明
     - 三個主要端點：GET /activities、POST /activities/{activity_name}/signup、DELETE /activities/{activity_name}/unregister
     - 請求/回應格式、狀態碼、使用範例
     - 資料模型、錯誤處理、限制與注意事項

  5. **docs/Prompt-Output.md** - Prompt 輸出記錄
     - 用於記錄所有文字輸出成果的可追溯日誌
     - 遵循規範格式（時間、Scope、Prompt、Output、Notes）

- **Notes**:
  - 所有文件使用繁體中文撰寫
  - API 文件內容與實際程式碼（src/app.py）完全一致
  - 設定文件反映應用程式的實際預設行為
  - 安裝指南涵蓋開發與生產環境設定建議

