# 設定指南

## 應用程式設定

本應用程式目前採用簡化設計，無需複雜的設定檔案。所有功能使用預設值執行。

## 伺服器設定

應用程式在啟動時使用以下預設設定：

- **主機：** `0.0.0.0`（監聽所有網路介面）
- **埠口：** `8000`（可透過命令列參數修改）
- **熱重載：** 啟用（開發環境自動重新載入程式碼變更）

### 自訂伺服器埠口

執行應用程式時，可使用 `--port` 參數修改埠口：

```bash
python -m uvicorn app:app --port 9000
```

### 生產環境設定

在生產環境中執行時，請禁用熱重載：

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 活動資料

應用程式在啟動時，自動載入預設的 9 個活動：

1. **國際象棋俱樂部** - Chess Club
2. **程式設計課程** - Programming Class
3. **體操課程** - Gym Class
4. **足球隊** - Soccer Team
5. **籃球隊** - Basketball Team
6. **美術俱樂部** - Art Club
7. **戲劇俱樂部** - Drama Club
8. **數學俱樂部** - Math Club
9. **辯論隊** - Debate Team

### 資料持久性

目前應用程式使用**記憶體內儲存**（in-memory storage），這表示：

- 所有活動與參與者資訊儲存在伺服器記憶體中
- 伺服器重啟後，資料將重置為預設狀態
- 適用於開發與測試環境
- **不適用於生產環境**需永久保存資料的情況

若需在生產環境中持久保存資料，需整合資料庫（如 PostgreSQL、MongoDB 等）。

## 跨域資源共享（CORS）

應用程式未明確設置 CORS 限制。在生產環境中部署前，建議：

1. 設置合適的 CORS 原點白名單
2. 透過 FastAPI 的 CORSMiddleware 配置 CORS 策略

## 日誌設定

應用程式日誌輸出到標準輸出（stdout）。Uvicorn 伺服器預設會記錄所有 HTTP 請求。

### 啟用詳細日誌

執行時加入 `--log-level` 參數：

```bash
python -m uvicorn app:app --log-level debug
```

可選的日誌級別：`critical`, `error`, `warning`, `info`, `debug`

## 最大參與者數限制

每個活動最多可容納的參與者數受其 `max_participants` 限制（於應用程式原始碼中定義）。嘗試報名超過限制的活動將返回錯誤。
