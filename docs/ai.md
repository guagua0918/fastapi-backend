# W01
## 1. 本週 Project Goal

建立 FastAPI 後端骨架，能啟動服務、用 `/docs` 測試 API，並理解 venv、REST、Swagger 這三個基礎概念。

## 2. 本週完成

- 建立 FastAPI 專案、`venv`、`requirements.txt`、`.gitignore`、`.env.example`
- 實作 `/api/health`、`/api/version`、`POST /api/items`
- 能開啟 Swagger `/docs` 並觀察 422 驗證錯誤

## 3. 問 AI 的三個重要問題

- Q1 為何後端需要 venv：學到 Python 依賴要專案隔離
- Q2 REST API 是什麼：學到用 HTTP 方法操作資源
- Q3 Swagger 是什麼：學到自動產生的 API 說明與測試頁

### Q1

- Prompt:
為何只有後端程式需要venv？
- AI 建議摘要:
`venv` 是 Python 的專案專用套件沙盒。後端用 `pip install fastapi uvicorn` 會裝很多套件；若裝進系統 Python，不同專案版本會互相打架。前端這階段主要是 HTML/CSS（之後才是 npm 的 `node_modules`），不跑 Python，所以不需要 Python venv。
- 我驗證的方法:
看 repo 裡有 `venv/` 且已被 `.gitignore` 忽略。
- 最後我採用 / 修改 / 拒絕了什麼:
採用「每個 Python 專案一個 venv」；前端誤建的 venv 已刪除，不把 venv 提交到 GitHub。

### Q2

- Prompt:
REST API 是什麼？
- AI 建議摘要:
REST API 是一種用 HTTP 存取「資源」的約定：用 URL 指資源、用方法表示動作（GET 讀、POST 建、PUT/PATCH 改、DELETE 刪），常見回傳 JSON。打開網頁多半拿 HTML 給人看；呼叫 API 多半拿資料給程式用。
- 我驗證的方法:
在 `/docs` 呼叫 `GET /api/health` 得到 JSON；`POST /api/items` 送 `{ "name": "...", "price": 1 }` 看回應。
- 最後我採用 / 修改 / 拒絕了什麼:
採用把 API 放在 `/api/...`，與前端頁面路徑分開。

### Q3

- Prompt:
Swagger 是什麼？為什麼 FastAPI 會有 `/docs`？
- AI 建議摘要:
Swagger UI 是 API 文件與測試介面；FastAPI 依程式碼自動產生 OpenAPI 規格，並提供 `/docs` 頁面，可直接試 GET/POST，不必先寫前端。
- 我驗證的方法:
啟動服務後打開 `/docs`，確認看得到 health、version、items；故意傳錯型別，觀察 422。
- 最後我採用 / 修改 / 拒絕了什麼:
採用先用 `/docs` 驗證 API，再接前端；把 Swagger 當本週主要測試工具。

## 4. Web Concept of the Week

後端是「常駐的程式」：收到 HTTP 請求 → 處理 → 回傳回應。  
`venv` 隔離依賴；REST 描述 API 怎麼設計；Swagger/`/docs` 讓人不用先做畫面就能測 API。

## 5. Debugging Record

- Problem:

- Error / symptom:

- Root cause:

- How I found it:

- Fix:

## 6. Security Check
- `venv/` 不進 Git（太大且與本機路徑有關）
- `.env` 不進 Git；只提交 `.env.example`
- Public repo 上的 API 文件也可能暴露端點設計，之後要考慮認證與授權

## 7. Reflection (反思)
這周是先搞懂後端服務怎麼被呼叫。有 `/docs` 後可以先確認API行為，再談前端。

- AI 哪裡講錯、講不清楚或讓我誤判：
我在前端也用了venv，最後提交的時候才告訴我這怪怪的。
- 如果下次自己做，我會：
先詢問，再新增檔案。

---

# W02
## 1. 本週 Project Goal
讓 PostgreSQL 可連線，用 `.env` 管理連線，並用 API 讀取 `notes`。

## 2. 本週完成
- [x] 啟動 ZIP PostgreSQL（5433）、`dev_user` / `fastapi_dev`
- [x] `.env` + `db_test.py` 測連線；`notes` 表與 3 筆資料
- [x] `GET /api/note/{id}`；學會用 venv 跑 Python

## 3. 問 AI 的三個重要問題
- [x] Q1 什麼要 venv、什麼不用
- [x] Q2 `pg_ctl` 相對路徑為何失敗
- [x] Q3 PowerShell 如何啟用 venv

### Q1
- Prompt: 哪些指令要進 venv？哪些不用？前面沒在 venv 跑 pg_ctl 要重做嗎？
- AI 建議摘要: `pg_ctl` / `psql` 不用 venv（管資料庫）。`pip`、`db_test.py`、`run.bat`／uvicorn 要 venv（管 Python 套件）。沒在 venv 跑開停 DB 沒關係，不必為此重做。
- 我驗證的方法: `(venv)` 下跑 `pg_ctl status` 仍正常；用 `venv\Scripts\python.exe` 跑 `db_test.py` 才保證套件正確。
- 最後採用: 開 DB 用完整路徑即可；測連線／跑 API 一定進 venv。

### Q2
- Prompt: 在 `fastapi-backend` 跑 `.\bin\pg_ctl.exe` 為何失敗？
- AI 建議摘要: `.\bin` 相對「目前資料夾」。`pg_ctl` 在 `%USERPROFILE%\pgsql\bin`。
- 我驗證的方法: 錯誤顯示找不到檔案；改 `cd pgsql` 或用完整路徑後成功。
- 最後採用: 開 DB 用完整路徑；跑 Python 才留在專案目錄。

### Q3
- Prompt: `activate venv` 為何無效？正確指令？
- AI 建議摘要: Windows PowerShell 用 `.\venv\Scripts\Activate.ps1`。
- 我驗證的方法: 啟用後出現 `(venv)`；再用 `python app\core\db_test.py`。
- 最後採用: 裝套件／測 DB／跑 API 都進 venv（或不 activate，直接用 `venv\Scripts\python.exe`）。

## 4. Web Concept of the Week
流程：`pg_ctl start` → `psql` 建表 → `.env` → `(venv) db_test.py` → FastAPI `GET /api/note/{id}`。  
`psql` 裡只打 SQL；`\q` 後才能打 PowerShell。

## 5. Debugging Record
- Problem: 在專案目錄執行 `.\bin\pg_ctl.exe`
- Error: 找不到 `.\bin\pg_ctl.exe`
- Root cause: 人在 `fastapi-backend`，不是 `pgsql`
- Fix: `cd $env:USERPROFILE\pgsql` 或 `"$env:USERPROFILE\pgsql\bin\pg_ctl.exe"`

## 6. Security Check
- `.env` 不進 Git；教學用 `dev_password` 僅本機
- SQL 用 `%s` 參數化，避免拼接注入
- `/api/note/{id}` 尚未做登入（之後再補）

## 7. Reflection (反思)
搞懂「目錄不對指令就失效」和 venv／psql／pg_ctl 各自管什麼。
- AI 誤判風險: 一次幫做完會學不到；應自己打指令再對答案。
- 下次: 先確認 `pwd`，再決定用相對路徑還是完整路徑。

---
