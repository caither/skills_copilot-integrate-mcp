# API 參考文件

Mergington 高中活動管理 API 提供簡單的 RESTful 介面，用於查詢活動和管理學生報名。

## 基礎資訊

- **基礎 URL：** `http://localhost:8000`
- **預設埠口：** `8000`
- **回應格式：** JSON

## API 端點

### 取得所有活動

### `GET /activities`

取得所有活動的清單，包括各活動的參與者清單與詳細資訊。

**請求：**

```bash
curl http://localhost:8000/activities
```

**回應：**

```json
{
  "activities": [
    {
      "name": "Chess Club",
      "description": "Learn and play chess",
      "schedule": "Monday 3:00 PM",
      "max_participants": 20,
      "participants": [
        "alice@mergington.edu",
        "bob@mergington.edu"
      ]
    },
    {
      "name": "Programming Class",
      "description": "Learn to code",
      "schedule": "Tuesday 4:00 PM",
      "max_participants": 30,
      "participants": []
    }
  ]
}
```

**狀態碼：**
- `200`：成功

---

### 學生報名活動

### `POST /activities/{activity_name}/signup`

為指定學生報名指定活動。若學生已報名或活動已滿，將返回錯誤。

**請求：**

```json
{
  "email": "student@mergington.edu"
}
```

**請求路徑參數：**
- `activity_name` (string)：活動名稱（英文版本，如 "Chess Club"）

**請求體：**
- `email` (string)：學生的電子郵件地址（格式：`name@mergington.edu`）

**範例：**

```bash
curl -X POST http://localhost:8000/activities/Chess%20Club/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "charlie@mergington.edu"}'
```

**成功回應（201）：**

```json
{
  "message": "Student charlie@mergington.edu signed up for Chess Club"
}
```

**錯誤回應：**

狀態碼 `400`（客戶端錯誤）：

```json
{
  "detail": "Activity 'Unknown Activity' not found"
}
```

```json
{
  "detail": "Student charlie@mergington.edu is already signed up for Chess Club"
}
```

```json
{
  "detail": "Activity 'Chess Club' is full"
}
```

**狀態碼：**
- `201`：報名成功
- `400`：錯誤的請求（活動不存在、學生已報名、活動已滿）

---

### 學生退出活動

### `DELETE /activities/{activity_name}/unregister`

為指定學生退出指定活動。若學生未報名該活動，將返回錯誤。

**請求：**

```json
{
  "email": "student@mergington.edu"
}
```

**請求路徑參數：**
- `activity_name` (string)：活動名稱（英文版本，如 "Chess Club"）

**請求體：**
- `email` (string)：學生的電子郵件地址

**範例：**

```bash
curl -X DELETE http://localhost:8000/activities/Chess%20Club/unregister \
  -H "Content-Type: application/json" \
  -d '{"email": "charlie@mergington.edu"}'
```

**成功回應（200）：**

```json
{
  "message": "Student charlie@mergington.edu unregistered from Chess Club"
}
```

**錯誤回應：**

狀態碼 `400`（客戶端錯誤）：

```json
{
  "detail": "Activity 'Unknown Activity' not found"
}
```

```json
{
  "detail": "Student charlie@mergington.edu is not signed up for Chess Club"
}
```

**狀態碼：**
- `200`：退出成功
- `400`：錯誤的請求（活動不存在、學生未報名）

---

### 重導到前端

### `GET /`

將使用者重導到前端應用程式。

**回應：**
- 重導到 `/static/index.html`

**狀態碼：**
- `307`：臨時重導

---

## 資料模型

### Activity（活動）

```json
{
  "name": "string",
  "description": "string",
  "schedule": "string",
  "max_participants": "integer",
  "participants": ["string"]
}
```

- `name`：活動名稱
- `description`：活動描述
- `schedule`：活動時間安排
- `max_participants`：最大參與者數
- `participants`：已報名學生的電子郵件清單

### SignupRequest（報名請求）

```json
{
  "email": "string"
}
```

- `email`：學生的電子郵件地址（格式：`name@mergington.edu`）

---

## 使用範例

### 範例 1：取得所有活動

```bash
curl http://localhost:8000/activities
```

### 範例 2：報名活動

```bash
curl -X POST http://localhost:8000/activities/Chess%20Club/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@mergington.edu"}'
```

### 範例 3：退出活動

```bash
curl -X DELETE http://localhost:8000/activities/Chess%20Club/unregister \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@mergington.edu"}'
```

---

## 錯誤處理

API 遵循標準 HTTP 狀態碼：

- `200`：請求成功
- `201`：資源已建立
- `400`：請求格式錯誤或邏輯錯誤
- `404`：資源未找到
- `500`：伺服器內部錯誤

所有錯誤回應都包含 `detail` 欄位，說明錯誤原因。

---

## 限制與注意事項

- 活動名稱區分大小寫
- 電子郵件地址應遵循 `name@mergington.edu` 格式
- 應用程式使用記憶體內儲存，伺服器重啟後資料將重置
- 同一學生可報名多個不同的活動
- 重複報名同一活動將返回錯誤
