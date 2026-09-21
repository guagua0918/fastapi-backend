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

`pg_ctl`：管「伺服器開或關」
`psql`：管「連進去下指令」
| | `pg_ctl` | `psql` |
|---|---|---|
| 比喻 | 開門／關門 | 進門辦事 |
| 典型指令 | start / stop / status | SELECT / CREATE / `\q` |
| 你在哪打 | PowerShell | 進入後的 `postgres=#` / `fastapi_dev=>` |

順序永遠是：

```text
pg_ctl start  →  psql 連線做事  →  （用完可）psql \q  →  （不需要時）pg_ctl stop
```

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
---

# W03
## 1. 本週 Project Goal
用 FastAPI 同時服務前端靜態頁與 `/api`，經 IIS 公開 HTTPS，並能解釋Swagger／快取／資料庫連線問題。

## 2. 本週完成
- [x] `run.bat`：`0.0.0.0:7777`；靜態根目錄 `webui-lab`；API 在 `/api`
- [x] 公開 `https://demo.wke.csie.ncnu.edu.tw/s115321503/`；Swagger 改到 `/api/docs`（相對路徑載入 openapi）
- [x] 用 Swagger 測 `items`／`note`；弄清連線在 `.env` 的 `DATABASE_URL`

## 3. 問 AI 的三個重要問題
- [x] Q1 程式跑在哪？為何沒開視窗也在跑？
- [x] Q2 為何 `/docs` 空白／老師是 `/api/docs`？無 `/` 排版為何壞？
- [x] Q3 `note` 沒回應？連線資訊在哪？`main.py` 怎麼讀 DB？

### Q1
- Prompt: 我沒開 run.bat，公開網址為何還進得去？行程在哪？
- AI 建議摘要: 真正跑網站的是本機 uvicorn（7777）；IIS 只反向代理。可能是先前背景啟動的 `run.bat`，沒有標題視窗所以找不到。關掉後 demo 會掛。
- 我驗證的方法: 查 port 7777 的 PID／命令列有 `uvicorn`；`GET /guide.html` 出現在終端機 log。
- 最後採用: 要公開測就自己開終端機跑 `.\run.bat`；停用 Ctrl+C 或結束該 python／cmd。

### Q2
- Prompt: 老師 `/api/docs` 有內容，我的 `/docs` 顯示 Failed to load openapi.json；網址無結尾 `/` 排版跑掉？
- AI 建議摘要: FastAPI 預設文件在 `/docs`；子路徑下瀏覽器去抓網站根的 `/openapi.json` 會 404。改掛 `/api/docs` 並用相對路徑 `openapi.json`。無 `/` 時相對 CSS 會解析到錯誤目錄，應使用 `.../s115321503/`。
- 我驗證的方法: 本機 `/api/docs`、`/api/openapi.json` 200；公開用有 `/` 的網址；304 代表快取未改檔。
- 最後採用: 文件網址用 `/api/docs`；對外連結一律帶尾斜線；改靜態檔用無痕或 Disable cache。

### Q3
- Prompt: note 無回復；如何測 items／note？
- AI 建議摘要: `main.py` 的 note 只負責查表。DB 沒開會一直等（像沒回應）。items 不需 DB；note 需要正確 id（我的資料是 7/8/9 不是 1）。
- 我驗證的方法: `pg_ctl status`；Swagger 測 POST `/api/items` 與 GET `/api/note/7`。
- 最後採用: 測 note 前先開 PostgreSQL；用 `SELECT id FROM notes` 確認 id。

## 4. Web Concept of the Week
```text
瀏覽器 →（HTTPS）IIS →（HTTP）本機 uvicorn:7777
         ├─ 靜態：webui-lab 的 html/css
         └─ /api/...：JSON（note 再連 PostgreSQL）
```
304 = 瀏覽器用快取；不是錯誤。

## 5. Debugging Record
- Problem: Swagger「Failed to load API definition」／note 無回應
- Error: 404 `/openapi.json`；或連線逾時；或 404 Note not found
- Root cause: 子路徑相對／絕對路徑；DB 未啟動；id 不存在
- Fix: `/api/docs` + 相對 openapi；`pg_ctl start`；改測存在的 note id

## 6. Security Check
- `.env`（含 DATABASE_URL）不進 Git
- 靜態檔限制 html/css，減少誤公開其他檔
- 公開 `/api/docs` 會暴露 API 形狀，之後需認證／授權

## 7. Reflection (反思)
空白多半是 openapi 路徑錯。
- 下次: 公開測前記得 run.bat + DB；Swagger 用 `/api/docs`；note 先查 id。

---
