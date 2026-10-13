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

# W04
## 1. 本週 Project Goal
把 notes 做成完整 REST CRUD，並把 API 拆成路由、資料格式、SQL、連線四層。

## 2. 本週完成
- [x] `POST/GET/PUT/DELETE /api/notes`；找不到 404，新增 201，刪除 204
- [x] `schemas`／`routers`／`repositories`；SQL 仍用 `psycopg`，細節見 `docs/architecture.md`
- [x] Swagger `/api/docs` 測過 `POST /api/notes` 回 201

## 3. 問 AI 的三個重要問題
- [x] Q1 一次 `POST /api/notes` 依序經過哪些檔？各管什麼？
- [x] Q2 Swagger 一直轉圈圈，是哪裡卡住？
- [x] Q3 `main.py` 對 notes 做了什麼、沒做什麼？

### Q1
- Prompt: 一次 `POST /api/notes` 會依序經過哪幾個檔？各管什麼？201／200／404 是不是都在路由層？
- AI 建議摘要: `main.py` 掛路由 → `routers/notes.py`（方法與狀態碼）→ `schemas/notes.py`（檢查 body）→ `repositories/notes.py`（SQL）→ `core/db.py`（連線）。201、200、204、404 在 router。422 是 schema 驗證失敗，函式本體還沒執行。repository 找不到只回 `None`。
- 我驗證的方法: `POST /api/notes` 回 201；少欄位時 Swagger 顯示 422。
- 最後採用: 狀態碼不寫進 SQL 那一層。

### Q2
- Prompt: 一直在轉圈圈。
- AI 建議摘要: `/api/docs` 已 200，轉的是 notes API 在連資料庫。`.env` 指向 5433，那套 PostgreSQL 沒開，`psycopg` 會等到逾時。5432 是另一套，連錯埠也沒用。
- 我驗證的方法: log 出現 `connection timeout` port 5433；`pg_ctl start` 之後 `POST /api/notes` 201。
- 最後採用: 測 notes 前先開 5433，`run.bat` 不要關。

### Q3
- Prompt: `main.py` 對 notes 做了什麼、沒做什麼？
- AI 建議摘要: 只 `include_router`，把 `/notes` 掛成 `/api/notes`。查詢、新增、刪除的 SQL 在 repository，不寫在 `main.py`。
- 我驗證的方法: `main.py` 沒有 `SELECT`／`INSERT`；`POST /api/notes` 仍回 201。
- 最後採用: `main.py` 當入口；notes 邏輯留在 router 與 repository。

## 4. Web Concept of the Week
```text
/api/notes
  → routers/notes.py      方法、狀態碼
  → schemas/notes.py      NoteCreate／NoteResponse
  → repositories/notes.py SQL（%s）
  → core/db.py            DATABASE_URL
```

## 5. Debugging Record
- Problem: Swagger 一直轉
- Error: connection timeout，port 5433
- Root cause: ZIP PostgreSQL 沒在跑；FastAPI 仍在 7777
- Fix: `pg_ctl start` 後再測

## 6. Security Check
- `.env` 不進 Git
- SQL 用 `%s`，不把使用者輸入拼進字串
- CRUD 尚未做登入

## 7. Reflection (反思)
分層是為了改 SQL 時不用翻 HTTP。轉圈先看資料庫有沒有開，不要先改路由。
- 下次: 5433 與 `run.bat` 都開著再進 `/api/docs`。

---

# W05
## 1. 本週 Project Goal
用 `insertClass` 長目錄樹，用 view 把 JOIN 存成 `vd_subclass`，再提供 `GET /api/subclass/pcid/{id}`。

## 2. 本週完成
- [x] `public` 的 `class`、`inheritance`、`object`、`co`
- [x] 目錄：首頁 → hahahan → 掃描、運動菜單、運動
- [x] `vd_subclass` 與 `GET /api/subclass/pcid/1`
- [x] 刪掉舊的 `i3s` schema，之後只用上課這套

## 3. 問 AI 的三個重要問題
- [x] Q1 我沒有 GRANT 為什麼還查得到 view？
- [x] Q2 `/api/subclass/pcid/1` 怎麼一路變成 JSON？
- [x] Q3 `public.class` 和以前的 `i3s.class` 是同一張表嗎？

### Q1
- Prompt:
為什麼我沒做 `GRANT SELECT ON vd_subclass`，用 hahahan 還是查得到？講義說的 API 最小授權到底在分什麼？
- AI 建議摘要:
建表、建 view 的人是擁有者，本來就能 SELECT，不用再授權給自己。最小授權是給另一個權限較小的 API 帳號：只 `GRANT SELECT` 這張 view，不把 `class` 的刪改權限一起給出去。
- 我驗證的方法:
用 hahahan 執行 `SELECT * FROM vd_subclass WHERE pcid = 1`，看得到掃描、運動菜單、運動。
- 最後我採用 / 修改 / 拒絕了什麼:
採用擁有者自己查不必 GRANT；之後若 API 改用別的帳號，再只授 view 的 SELECT。

### Q2
- Prompt:
`GET /api/subclass/pcid/1` 從網址到 JSON 經過哪些檔？repository 為什麼不自己寫 `psycopg.connect`？
- AI 建議摘要:
`main.py` 把 subclass router 掛在 `/api`。`routers/subclass.py` 接到路徑，取出 `pcid=1`，呼叫 repository。repository 用 `get_connection()`，連線字串在 `.env`，由 `core/db.py` 讀。SQL 是 `SELECT ... FROM vd_subclass WHERE pcid = %s`。`schemas/subclass.py` 規定回傳 `pcid`、`parent_name`、`cid`、`child_name`。
- 我驗證的方法:
重啟 FastAPI 後開 `/api/subclass/pcid/1`，JSON 裡有掃描、運動菜單、運動。對過 router 沒有自己組目錄名稱。
- 最後我採用 / 修改 / 拒絕了什麼:
採用跟 notes 一樣分層；SQL 留在 repository，不寫進 `main.py`。

### Q3
- Prompt:
`public.class` 跟我之前建的 `i3s.class` 是同一張表嗎？沒寫 schema 時 `SELECT * FROM class` 會打到哪一套？
- AI 建議摘要:
不是同一張。完整名字是 `schema.表`。W05 這套在 `public`；舊的六張表在 `i3s`。沒寫 schema 時走預設 `search_path`，也就是 `public.class`。
- 我驗證的方法:
`\dt` 看到 `public.class` 與當時的 `i3s.class` 同時存在；查 `class` 得到的是首頁、hahahan 那套。
- 最後我採用 / 修改 / 拒絕了什麼:
採用只留上課的 `public` 表，並刪掉 `i3s` schema。

## 4. Web Concept of the Week
View 是存好的 JOIN，不是另一份資料。API 只對 `vd_subclass` 下 `SELECT`。

## 5. Debugging Record
- Problem: `psql` 連 5433 被拒絕
- Error: connection refused
- Root cause: ZIP 版 PostgreSQL 沒在跑
- Fix: `pg_ctl -D pgsql-data -o "-p 5433" start`

## 6. Security Check
- `.env` 不進 Git
- API 用 `%s` 傳 `pcid`，不把網址參數拼進 SQL
- 擁有者與最小授權是兩件事；API 若換帳號，只授 view 的 SELECT

## 7. Reflection (反思)
目錄先長在 `class` / `inheritance`，查詢交給 view，HTTP 只負責把 `pcid` 傳進去。
- 下次: 先確認連到的是 `public.class`，不要和別的 schema 搞混。

---

# W06
## 1. 本週 Project Goal
用 Google 登入證明是誰，由自己的後端發 JWT，放進 HttpOnly cookie，並讓 `notes`、`subclass` 沒登入就回 401。

## 2. 本週完成
- [x] `member` 表，`google_sub` 唯一
- [x] `GET /api/auth/google/login`、`callback`、`/api/auth/me`、`POST /api/auth/logout`
- [x] 登入後簽自己的 JWT，cookie 名稱 `access_token`
- [x] `notes`、`subclass` 未登入回 401
- [x] 右上角未登入顯示登入，登入後顯示 Gmail 名稱和頭貼

## 3. 問 AI 的三個重要問題
- [x] Q1 網站問我允不允許 cookie，和登入那張是同一個東西嗎？
- [x] Q2 登出之後，被拿走的 JWT 還能不能用？
- [x] Q3 人去 Google 改了信箱，會多一列會員嗎？

### Q1
- Prompt:
平常進入網站會問我允不允許紀錄 cookie。那和登入之後瀏覽器自動帶回去的是同一個東西嗎？我的後端現在會設哪幾張？
- AI 建議摘要:
是同一種 cookie：伺服器用 `Set-Cookie` 請瀏覽器保存一小段字串，之後對同一個網站的請求會自動放進 `Cookie` 標頭。彈窗多半在問要不要再存廣告或流量統計。登入這兩張是自己要求登入才有的，不靠那個彈窗。`session` 在跳去 Google 之前寫入，裡面是 OAuth 的 `state`。`access_token` 在 callback 成功時寫入，裡面是自己簽的 JWT，HttpOnly，JavaScript 讀不到原文。
- 我驗證的方法:
看 `app/routers/auth.py` 的 `set_cookie`（名稱 `access_token`、`httponly=True`）和 `app/main.py` 的 `SessionMiddleware`。頁面上沒有「允許 cookie」按鈕，也沒有統計用的 cookie。
- 最後我採用 / 修改 / 拒絕了什麼:
採用只設登入用的兩張 cookie，不做追蹤，也不做允許彈窗。

### Q2
- Prompt:
登出是不是只把瀏覽器裡的 `access_token` 刪掉？這張 JWT 在過期前已經被別人拿到的話，我登出之後他還能不能打 `/api/auth/me`？後端有沒有一份已作廢清單？
- AI 建議摘要:
登出只下 `delete_cookie`，資料庫沒有作廢清單。`/api/auth/me` 只檢查簽名、`iss`、`exp`，再拿 `sub` 查 `member`。票還在效期內、人也還在，就回 200。要讓它立刻失效，得另做作廢清單，或把效期縮短。
- 我驗證的方法:
看 `logout` 只有 `delete_cookie(COOKIE_NAME)`。`get_current_member` 沒有查「這張票是否已登出」。
- 最後我採用 / 修改 / 拒絕了什麼:
採用目前只刪瀏覽器裡的 cookie。知道被拿走的 JWT 在過期前仍然有效；這次沒加作廢清單。

### Q3
- Prompt:
`member` 為什麼用 `google_sub` 當唯一鍵，不用 email？我到 Google 把信箱改掉再登入一次，會多一列，還是同一列把 email 換掉？
- AI 建議摘要:
Google 的 `sub` 是這個帳號的固定編號，不跟著信箱改。唯一鍵放 `google_sub` 時，再登入走 `ON CONFLICT (google_sub) DO UPDATE`，同一列的 `email`、`name`、`picture` 被更新。
- 我驗證的方法:
看 `psql/member.sql` 的 `google_sub text NOT NULL UNIQUE`，以及 `upsert_google_member` 的 `ON CONFLICT (google_sub) DO UPDATE` 會改 `email`。學校站登入成功後，`member` 只有 1 列。
- 最後我採用 / 修改 / 拒絕了什麼:
採用 `google_sub` 當唯一鍵，再次登入更新同一列，不用 email 去判斷是不是同一個人。

## 4. Web Concept of the Week
Google 證明這個人是誰。自己的後端發 JWT，放在 HttpOnly cookie 裡。之後 `/api/auth/me` 認的是這張票。

## 5. Debugging Record
- Problem: 加上 `SessionMiddleware` 後服務起不來
- Error: `ModuleNotFoundError: itsdangerous`
- Root cause: session cookie 需要這個套件，當時 venv 還沒裝完
- Fix: 安裝 `itsdangerous` 後重新啟動；`GET /api/auth/google/login` 回 302

## 6. Security Check
- `.env` 不進 Git；JWT 與 session 用兩把不同的鑰匙
- JWT 放 HttpOnly cookie，頁面腳本讀不到原文
- 登出只刪 cookie，效期內被複製走的票仍然有效
- cookie 路徑是 `/`，和同學共用學校網域時，瀏覽器會把 `access_token` 送到其他學號路徑；對方沒有這把鑰匙就驗不過，但字串已經出現在對方的請求裡

## 7. Reflection (反思)
登入分兩段：Google 的 `userinfo` 只用來建立或更新 `member`；之後每個 API 只認自己簽的 JWT。
- 下次: 若要讓登出立刻作廢，再加作廢清單；cookie 路徑改成自己的 `/s115321503`。

---
