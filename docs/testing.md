# 測試文檔

## 概述
此項目使用 **pytest** 進行單元測試和集成測試，實現完整的代碼覆蓋率。

## 測試統計
- **測試總數**: 16
- **通過**: 16 ✅
- **失敗**: 0
- **代碼覆蓋率**: **100%**

## 測試結構

### 1. 根端點測試 (Root Endpoint Tests)
- `test_root_redirects_to_static`: 驗證根路徑重定向到 `/static/index.html`

**覆蓋**: `GET /` 端點

### 2. 獲取活動測試 (Get Activities Tests)
- `test_get_all_activities`: 驗證返回所有 9 個活動
- `test_get_activities_contains_all_expected`: 驗證包含所有預期的活動
- `test_activity_structure`: 驗證每個活動的結構完整性

**覆蓋**: `GET /activities` 端點

### 3. 報名測試 (Signup Tests)
- `test_successful_signup`: 驗證成功報名
- `test_signup_nonexistent_activity`: 驗證報名不存在的活動返回 404
- `test_signup_duplicate_student`: 驗證重複報名被拒絕
- `test_signup_different_students`: 驗證多個學生可報名同一活動

**覆蓋**: `POST /activities/{activity_name}/signup` 端點

### 4. 退登測試 (Unregister Tests)
- `test_successful_unregister`: 驗證成功退登
- `test_unregister_existing_student`: 驗證移除已報名的學生
- `test_unregister_nonexistent_activity`: 驗證退登不存在的活動返回 404
- `test_unregister_not_signed_up_student`: 驗證未報名學生退登返回 400

**覆蓋**: `DELETE /activities/{activity_name}/unregister` 端點

### 5. 集成測試 (Integration Tests)
- `test_signup_and_unregister_flow`: 驗證完整報名和退登流程
- `test_multiple_signups_same_student`: 驗證學生可報名多個活動

**覆蓋**: 多個端點的協同工作

### 6. 邊界情況測試 (Edge Cases)
- `test_signup_with_special_characters_email`: 驗證特殊字符郵箱
- `test_activity_name_case_sensitive`: 驗證活動名稱對大小寫敏感

**覆蓋**: 特殊輸入和邊界條件

## 運行測試

### 運行所有測試
```bash
pytest tests/test_app.py -v
```

### 運行特定測試類
```bash
pytest tests/test_app.py::TestSignup -v
```

### 運行特定測試
```bash
pytest tests/test_app.py::TestSignup::test_successful_signup -v
```

### 生成覆蓋率報告
```bash
pytest tests/test_app.py --cov=src --cov-report=html
```
報告位置: `htmlcov/index.html`

### 使用配置文件運行
```bash
pytest
```

## 測試工具

### 依賴包
- **pytest**: Python 測試框架
- **pytest-cov**: 代碼覆蓋率工具
- **httpx**: 非同步 HTTP 客戶端（被 TestClient 使用）

### 安裝依賴
```bash
pip install -r requirements.txt
```

## 測試特性

### Fixtures
- `client`: 提供 FastAPI TestClient，用於 API 測試
- `reset_activities`: 重置活動數據到初始狀態，確保測試隔離

### 測試隔離
每個測試使用 `reset_activities` fixture，確保：
- 測試之間不相互干擾
- 每個測試都從乾淨的狀態開始
- 測試完成後自動清理

## 代碼覆蓋率詳情

```
Name         Stmts   Miss  Cover   Missing
------------------------------------------
src/app.py      33      0   100%
------------------------------------------
TOTAL           33      0   100%
```

### 覆蓋的代碼段
✅ 所有路由端點 (`@app.get`, `@app.post`, `@app.delete`)
✅ 所有錯誤處理 (HTTPException 拋出和捕獲)
✅ 所有業務邏輯 (驗證、數據操作)
✅ 所有邊界情況

## 連續集成 (CI) 建議

添加到 GitHub Actions 工作流:
```yaml
- name: Run tests with coverage
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## 最佳實踐

1. **運行完整測試**: 每次提交前運行所有測試
2. **檢查覆蓋率**: 確保新代碼有相應測試
3. **使用 Fixtures**: 確保測試隔離和可重複性
4. **清晰的測試名稱**: 測試名稱應清楚說明測試內容
5. **測試分類**: 使用類組織相關測試

## 調試測試

### 顯示詳細輸出
```bash
pytest tests/test_app.py -vv
```

### 顯示打印語句
```bash
pytest tests/test_app.py -s
```

### 運行特定標記的測試
```bash
pytest tests/test_app.py -m unit
```

### 在第一個失敗時停止
```bash
pytest tests/test_app.py -x
```

## 常見問題

### Q: 為什麼需要 `reset_activities` fixture?
A: 因為活動數據存儲在全局變量中，沒有持久化存儲。fixture 確保每個測試從相同的初始狀態開始。

### Q: 如何添加新測試?
A:
1. 在 `tests/test_app.py` 中創建新的測試方法
2. 使用描述性的名稱 (test_* 前綴)
3. 確保測試使用 `reset_activities` fixture
4. 運行 `pytest` 驗證

### Q: 如何提高代碼覆蓋率?
A: 當前已達到 100% 覆蓋率。對於新功能:
1. 為每個代碼路徑創建測試
2. 包括成功案例和錯誤情況
3. 測試邊界條件

## 相關文檔
- [pytest 官方文檔](https://docs.pytest.org/)
- [FastAPI 測試文檔](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py 文檔](https://coverage.readthedocs.io/)
