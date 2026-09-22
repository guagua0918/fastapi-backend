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
- [x] 啟動 ZIP PostgreSQL（埠可自訂）、開發帳號／庫
- [x] 本機 `.env` + `db_test.py` 測連線；`notes` 表與資料
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
- `.env` 不進 Git；文件只寫佔位符，不寫真實密碼
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
- [x] 公開 demo 學號子路徑；Swagger 改到 `/api/docs`（相對路徑載入 openapi）
- [x] 用 Swagger 測 `items`／`note`；連線只放本機 `.env` 的 `DATABASE_URL`

## 3. 問 AI 的三個重要問題
- [x] Q1 程式跑在哪？為何沒開視窗也在跑？
- [x] Q2 路由怎麼對到 `main.py`？為何無尾 `/` 會壞、Swagger 要改路徑？
- [x] Q3 `note` 沒回應？連線資訊在哪？`main.py` 怎麼讀 DB？

### Q1
- Prompt: 我沒開 run.bat，公開網址為何還進得去？行程在哪？
- AI 建議摘要: 真正跑網站的是本機 uvicorn（7777）；IIS 只反向代理。可能是先前背景啟動的 `run.bat`，沒有標題視窗所以找不到。關掉後 demo 會掛。
- 我驗證的方法: 查 port 7777 的 PID／命令列有 `uvicorn`；`GET /guide.html` 出現在終端機 log。
- 最後採用: 要公開測就自己開終端機跑 `.\run.bat`；停用 Ctrl+C 或結束該 python／cmd。

### Q2
- Prompt: 我不懂路由。請用 `main.py` 對應「公開網址 → 本機路徑」；並解釋無尾斜線排版壞掉、Swagger 空白。
- AI 建議摘要:
  - **路由**＝「這個 URL 路徑要叫哪個函式／哪個資料夾」。寫在 `@app.get(...)`、`@api_router...`、`app.mount(...)`。
  - IIS 先剝掉學號前綴（如 `/s學號`），uvicorn 只看到後面；例如公開 `.../s學號/api/note/7` → 本機 `/api/note/7` → `get_note`。
  - **尾斜線**：HTML 裡 `css/style.css` 是相對路徑。有 `/` 時目錄是 `.../s學號/`，CSS 正確；無 `/` 時瀏覽器把最後一段當檔名，CSS 會抓錯層。
  - **Swagger**：關掉預設 `/docs`，改 `@app.get("/api/docs")`，且 `openapi_url="openapi.json"`（相對）才會在子路徑下抓到 `/api/openapi.json`。
- 我驗證的方法: 有 `/` 的 demo 網址樣式正常；本機 `/api/docs` 可載入；對照 `main.py` 的 decorator／mount 與實際 URL。
- 最後採用: 對外一律帶尾斜線的學號路徑；文件用 `/api/docs`；先畫「URL → 哪一行程式」再改 bug。

### Q3
- Prompt: note 無回復；如何測 items／note？
- AI 建議摘要: `main.py` 的 note 只負責查表。DB 沒開會一直等（像沒回應）。items 不需 DB；note 需要正確 id（我的資料是 7/8/9 不是 1）。
- 我驗證的方法: `pg_ctl status`；Swagger 測 POST `/api/items` 與 GET `/api/note/7`。
- 最後採用: 測 note 前先開 PostgreSQL；用 `SELECT id FROM notes` 確認 id。

## 4. Web Concept of the Week

### 架構 ↔ `main.py`（路由在幹嘛）

```text
瀏覽器
  │  https://demo.../s學號/guide.html
  ▼
IIS（只轉送，剝掉學號前綴）
  │  轉成 → http://本機:7777/guide.html
  ▼
uvicorn（run.bat）讀 app.main:app
  │
  ├─ /api/docs          → @app.get("/api/docs") → swagger_ui()
  ├─ /api/openapi.json  → FastAPI 內建（openapi_url=...）
  ├─ /api/health 等     → api_router（prefix="/api"）→ include_router
  ├─ /api/note/{id}     → get_note() → get_connection() → PostgreSQL
  ├─ /                  → serve_index() → webui-lab/index.html
  └─ /guide.html、/css/... → app.mount("/", HtmlCssOnlyStaticFiles(...))
                              directory = webui-lab
```

對照表：

| 你開的網址（公開） | uvicorn 實際路徑 | 程式哪一段 |
|---|---|---|
| `.../s學號/` | `/` | `serve_index` 或 mount 的 index |
| `.../s學號/guide.html` | `/guide.html` | `HtmlCssOnlyStaticFiles` → 檔案 |
| `.../s學號/api/note/7` | `/api/note/7` | `@api_router.get("/note/{note_id}")` |
| `.../s學號/api/docs` | `/api/docs` | `@app.get("/api/docs")` |

`APIRouter(prefix="/api")`：路由器上寫 `/note/...`，掛上後完整路徑變成 `/api/note/...`。  
`app.mount("/", ...)`：上面沒被更精確路由吃掉的路徑，才丟給靜態檔。

### 為何 `HtmlCssOnlyStaticFiles` 是 class？

`StaticFiles` 已經會「依路徑讀檔回傳」。我們要**多一步檢查**：不是 `.html`／`.css` 就 404。

- 用 **class 繼承** `StaticFiles`，只覆寫 `get_response`：先自己過濾，再 `super().get_response(...)` 沿用原本讀檔邏輯。
- 之後 `app.mount(..., HtmlCssOnlyStaticFiles(directory=...))` 才能把「客製規則」掛進同一個靜態入口。
- 若只寫普通函式，掛不上 Starlette／FastAPI 期待的「靜態檔應用」介面。

### 尾斜線（相對路徑）

頁面裡若寫 `href="css/style.css"`（相對）：

| 網址列 | 瀏覽器怎麼組 CSS |
|---|---|
| `.../s學號/` | `.../s學號/css/style.css` ✓ |
| `.../s學號`（無 `/`） | 常變成錯層（把最後一段當檔名）✗ |

對外連結一律帶尾 `/`。304＝快取未改，不是錯誤。

## 5. Debugging Record
- Problem: Swagger「Failed to load API definition」／無 `/` 排版壞／note 無回應
- Error: 404 `/openapi.json`；CSS 路徑錯；連線逾時或 Note not found
- Root cause: 子路徑下絕對／相對路徑；尾斜線；DB 未啟動；id 不存在
- Fix: `/api/docs` + 相對 openapi；網址帶 `/`；`pg_ctl start`；改測存在的 note id

## 6. Security Check
- `.env`（含 DATABASE_URL）不進 Git
- `HtmlCssOnlyStaticFiles` 限制只出 html/css，減少誤公開其他檔
- 公開 `/api/docs` 會暴露 API 形狀，之後需認證／授權

## 7. Reflection (反思)
不懂路由時先對表：URL → `main.py` 哪一行。空白多半是 openapi 路徑錯；排版壞先查尾 `/`。
- 下次: 公開測前記得 run.bat + DB；Swagger 用 `/api/docs`；note 先查 id。

---
