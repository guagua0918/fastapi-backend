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

# W07
## 1. 本週 Project Goal
用 pytest + TestClient 自動測 Auth 門禁與 notes CRUD；沒有密碼登入就改測 JWT／scan 授權。

## 2. 本週完成
- [x] 安裝 `pytest`、`httpx`；新增 `tests/`
- [x] `conftest.py`：`client`（未登入）、`auth_client`（override 假會員）
- [x] 測 401、notes CRUD、scan 找不到／未登入；`pytest -v` 通過

## 3. 問 AI 的三個重要問題
- [x] Q1 測未登入 401 為什麼不能用 `auth_client`？
- [x] Q2 override 假裝登入，正式站會不會被繞過？
- [x] Q3 pytest 全綠＝整條產品都沒問題嗎？

### Q1
- Prompt:
`conftest` 有 `client` 跟 `auth_client`。我要測「沒登入應該 401」，為什麼不能用 `auth_client`？那它是給誰用的？
- AI 建議摘要:
`auth_client` 會用 `dependency_overrides` 把 `get_current_member` 換成假會員，請求看起來永遠已登入，測不到 401。測門禁用沒 override 的 `client`；測「登入後的 CRUD／／me」才用 `auth_client`，才不用真的走 Google。
- 我驗證的方法:
`test_auth.py` 裡 401 用 `client`；`test_me_with_override_returns_profile`、`test_notes.py` 用 `auth_client`。混用會讓 401 測試變假綠燈。
- 最後我採用 / 修改 / 拒絕了什麼:
採用兩種 fixture 分開：門禁用 `client`，業務用 `auth_client`。

### Q2
- Prompt:
測試可以 `dependency_overrides` 假裝已登入、不用走 Google。這樣正式網站會不會被別人繞過登入？算不算資安洞？
- AI 建議摘要:
不算。override 只活在「正在跑 pytest 的那個 Python 行程」裡，是測試輔助。對外的 uvicorn 不會掛這些 override，還是驗真 JWT；沒票仍 401。真正有風險的是把「永遠回假會員」寫進正式程式，或把 debug 開關留在 production。
- 我驗證的方法:
看 `conftest.py` 只在 fixture 裡設 override，測完 `clear()`。用未 override 的 `client` 打 `/api/auth/me` 仍是 401。
- 最後我採用 / 修改 / 拒絕了什麼:
採用測試用 override；正式環境不靠這招登入。

### Q3
- Prompt:
我 `pytest -v` 全綠了，能不能說 Google 登入跟 CV worker 算足印都沒問題？還缺什麼？
- AI 建議摘要:
不能。現有測試多半是門禁、notes CRUD、scan 的 401／404，用 override 假裝登入，沒跑真的 Google OAuth，也沒啟動 worker／SAM。全綠只代表「寫進測試的行為」OK，不是整條掃描 E2E。
- 我驗證的方法:
測試檔沒有打 `/api/auth/google/login`，也沒有等 `cv_keypoints_done`。掃描仍要自己開 `run.bat`、PG、`run_cv_worker.bat` 手動走一輪。
- 最後我採用 / 修改 / 拒絕了什麼:
採用 W07 先覆蓋 Auth＋CRUD／授權邊界；E2E 登入與 CV 當手動或之後再加測。

## 4. Web Concept of the Week
```text
pytest 收 test_* → TestClient 打 FastAPI
  → 測 401 用 client
  → 測登入後 API 用 auth_client（override，非正式後門）
```

## 5. Debugging Record
- Problem: 一開始 venv 沒有 pytest
- Error: `ModuleNotFoundError: No module named 'pytest'`
- Root cause: 尚未 `pip install pytest httpx`
- Fix: 裝進 `fastapi-backend\venv` 後再 `pytest -v`

## 6. Security Check
- 測試 override ≠ 線上免登入
- 未帶票／壞票應 401（有自動化覆蓋）
- notes 測試會碰開發 DB，測完刪自建列；進階可再拆測試庫

## 7. Reflection (反思)
自動化測的是「門禁與 CRUD 契約」；真登入與影像分析仍要手動或另寫 E2E。
- 下次: 若 notes 加上 `mid`，補「不能刪別人的 note」；可考慮獨立 `fastapi_test`。

---

# W08
## 1. 本週 Project Goal
用連線池共用 DB 連線；notes 改 async 等資料庫；搞清楚 I/O vs CPU，以及為什麼 SAM 仍留在 worker。

## 2. 本週完成
- [x] `psycopg_pool`：同步池給 scan／member／subclass；非同步池給 notes
- [x] `main.py` lifespan 開關池；Windows 用 SelectorEventLoop
- [x] notes router／repository 改 `async`；`test_pool_concurrent`；`pytest` 通過

## 3. 問 AI 的三個重要問題
- [x] Q1 為什麼 upload 不直接跑完 SAM？
- [x] Q2 連線池滿了，多出來的請求怎樣？
- [x] Q3 輪詢算 I/O 還是 CPU？若改 WebSocket 差在哪？

### Q1
- Prompt:
為什麼不在 `upload_foot` 裡直接把 SAM 跑完再回傳給前端？改成先標 `pending`、另開 CV worker，使用者體驗跟系統各得到什麼、失去什麼？
- AI 建議摘要:
SAM 是 CPU bound，塞進上傳 API 會佔住處理該請求的時間，別人的 API 也容易一起卡。改成 pending＋worker：上傳很快結束，分析在背景做；前端用輪詢看進度。得到：網站比較不容易被一張圖拖死、可重試／獨立重開 worker。失去：不能「一個 HTTP 結束就拿到點」；一定要多開 worker、多一次狀態機。
- 我驗證的方法:
`upload_foot` 只寫 `input.png` 與 `pending`；`cv_worker.process_one` 才跑 SAM。畫面上會先「分析中」再進確認頁。
- 最後我採用 / 修改 / 拒絕了什麼:
採用非同步排隊；拒絕在上傳請求裡同步跑完 SAM。

### Q2
- Prompt:
`DB_POOL_MAX_SIZE=10` 時，第 11 個也要借連線的請求是被拒絕，還是排隊？跟「網站當掉」差在哪？
- AI 建議摘要:
觀念上是**排隊等池子釋出連線**，不是把前 10 個踢掉，也通常不是立刻當整站。等太久才可能連線／請求逾時而失敗。網站當掉比較像行程崩潰、DB 掛了、或同步 CPU 把 event loop 堵死。池子滿＝暫時借不到連線，服務程序多半還在。
- 我驗證的方法:
看 `app/core/db.py` 的 `max_size`；`test_pool_concurrent` 並發打 health／notes 仍 200（負載不大時池子夠用）。
- 最後我採用 / 修改 / 拒絕了什麼:
採用 min=1、max=10 的池；知道滿了是等待不是「擠掉別人」。

### Q3
- Prompt:
前端一直 `GET /api/scan/footprints/{fid}` 輪詢，這算 I/O bound 還是 CPU bound？如果改成 WebSocket 由 worker 算完推播，觀念上差在哪？我現在有做 WebSocket 嗎？
- AI 建議摘要:
輪詢是 **I/O**：反覆等網路與 DB 讀狀態，幾乎不佔重 CPU。WebSocket 觀念上變成「伺服器有結果再推」，可少打很多次空的 GET，但要維護長連線與推播路徑；worker 仍可不直連瀏覽器，多半是 API 收到 DB 變化再推，或另做通知通道。我目前**沒做** WebSocket，仍用輪詢。
- 我驗證的方法:
`scan.js` 的 `pollFootprint`＋`setInterval`；專案裡沒有 WebSocket 路由。
- 最後我採用 / 修改 / 拒絕了什麼:
採用輪詢；WebSocket 當加分想像，這次不實作。

## 4. Web Concept of the Week
```text
I/O（等 DB／網路）→ 池子 + async notes
CPU（SAM）      → CV worker，不塞 upload API
瀏覽器 ↔ 只打 FastAPI；worker ↔ 只碰 DB／檔案
```

## 5. Debugging Record
- Problem: notes async 測試卡住
- Error: Psycopg cannot use the ProactorEventLoop
- Root cause: Windows 預設事件迴圈與 psycopg async 不相容
- Fix: `main.py`／`conftest.py` 設 `WindowsSelectorEventLoopPolicy`

## 6. Security Check
- 瀏覽器不直連 worker；資料進出仍經受 JWT 保護的 API
- 連線字串仍在 `.env`，不進 git

## 7. Reflection (反思)
這週重點是「等待」與「計算」分開：池／async 管等待；重計算留 worker。
- 下次: 若要少輪詢，再評估 WebSocket；先維持 pending 狀態機即可。

---

# W09
## 1. 本週 Project Goal
運動教學用進階查詢觀念：目錄篩選、關鍵字搜尋；重用 `vd_subclass`／`vd_objectlist`，並搞清楚查詢該放前端、API 還是 PostgreSQL，以及分頁何時需要。

## 2. 本週完成
- [x] `vd_objectlist`／`vd_object`；`GET /api/objectlist/cid/{cid}`、`GET /api/object/oid/{oid}`
- [x] W09 分頁／搜尋：`?q=&page=&size=` → `{items,total,page,size,total_pages}`；`ILIKE` 參數化；`offset=(page-1)*size`
- [x] 運動頁改打後端分頁＋關鍵字；多目錄條件仍可前端交集
- [x] 詳情步驟／YouTube iframe；列表縮圖（有影片用 YouTube thumb）

## 3. 問 AI 的三個重要問題
- [x] Q1 關鍵字要比對標題，前端過濾還是 PostgreSQL `ILIKE`？
- [x] Q2 多目錄條件要「兩個都符合」時，多次 objectlist 交集還是後端一條 SQL？
- [x] Q3 分頁的 OFFSET 怎麼算？資料很多時有什麼問題？運動頁現在要不要上分頁？

### Q1
- Prompt:
關鍵字要比對標題，我該在前端過濾，還是讓 PostgreSQL 用 `ILIKE`？兩邊各自適合什麼資料量？我現在運動列表只有十幾筆，選哪邊比較合理，之後變多要怎麼改？
- AI 建議摘要:
十幾筆可前端過濾，實作快、可重用已載入的 objectlist。資料變多、還要跟權限／分頁一起查，就改 API／DB 的 `ILIKE`，用參數化（`%s`），不要把字串拼進 SQL。`ILIKE '%x%'` 大量時可能較慢，但先求正確與安全。
- 我驗證的方法:
後來補上 API：`GET /api/objectlist/cid/5?q=提踵` 用 `ILIKE` 參數化，回傳的 `total`／`items` 與手動 SQL 一致；運動頁搜尋改帶 `q`。
- 最後我採用 / 修改 / 拒絕了什麼:
採用「VIEW 固定形狀＋API 動態 `q`／分頁」；關鍵字下推 PostgreSQL，不再只靠前端過濾。

### Q2
- Prompt:
一個動作會掛在好幾個目錄。使用者同時選兩個條件、「必須兩個都符合」要怎麼查？多次打 objectlist 再交集，跟後端一條 SQL 動態 WHERE，我該怎麼選？參數化要守什麼才不會被注入？
- AI 建議摘要:
AND 語意＝該 oid 在兩個 cid 的 `co` 都出現。多次 objectlist＋前端交集：API 單純、符合 reuse view，但多次往返、難做 total／分頁。一條 SQL（例如多個 `EXISTS ... cid = %s`）適合一次查完與分頁；使用者輸入只當參數值，欄位名若動態要用白名單。
- 我驗證的方法:
選兩個篩選後 Network 會看到多次 `/api/objectlist/cid/...`，結果是兩邊都有的動作；只選一個則等同單一目錄列表。
- 最後我採用 / 修改 / 拒絕了什麼:
採用多次 objectlist 交集以 reuse 現有 API；動態 SQL 當之後要分頁／放大資料量再考慮。

### Q3
- Prompt:
講義分頁要回 total、page、size。OFFSET 怎麼算？資料上到很多頁之後用 OFFSET 可能怎樣？什麼情況改用 Keyset／cursor？我的運動頁現在要不要上分頁？
- AI 建議摘要:
`offset = (page - 1) * size`；排序要固定。頁很深時 OFFSET 常變慢，中間增刪資料也可能讓頁面位移。無限捲動適合 Keyset（`WHERE id > last ORDER BY id LIMIT n`）。運動頁資料少可先不分頁；清單變長再在 API 做分頁，不要只切前端陣列假裝分完。
- 我驗證的方法:
`page=1&size=5` → OFFSET 0；`page=2` → OFFSET 5；回傳 `total=15`、`total_pages=3`。運動頁有上一頁／下一頁。
- 最後我採用 / 修改 / 拒絕了什麼:
採用 OFFSET 分頁（資料量小）；Keyset 先記觀念，這次不實作。

## 4. Web Concept of the Week
```text
VIEW：固定 JOIN／語意（vd_objectlist）— 不會自動分頁或動態 keyword
API：可動態 WHERE + LIMIT/OFFSET（之後若要）
前端：資料少時可先篩選／交集；資料多應下推 DB
Injection：使用者輸入只當參數值，不拼進 SQL 字串
```

## 5. Debugging Record
- Problem: 曾做自訂 `/api/exercise/search`，與講義「reuse subclass／objectlist」不一致
- Error: （設計／驗收方向偏離，非執行錯誤）
- Root cause: 為搜尋另開 API，沒先走 view＋既有端點
- Fix: 改回 `vd_objectlist`＋`/api/objectlist`；關鍵字與多條件先在前端處理

## 6. Security Check
- objectlist／object 仍走登入保護的 API
- 若日後 keyword 進 SQL，必須參數化；不可字串拼接

## 7. Reflection (反思)
W09 核心是「查詢放哪一層」：VIEW（`vd_objectlist`）管穩定形狀；`q`／`page`／`size` 在 API 參數化查詢。
- 下次: 多目錄 AND 也可下推成單次 SQL；若要交 EXPLAIN 再對 `vd_objectlist` 跑一次比較。

---

# W10
## 1. 本週 Project Goal
統一錯誤 JSON、請求 Logging middleware，未預期例外不把 stack 洩給前端。

## 2. 本週完成
- [x] `AppException`＋handler；`HTTPException` 也改成同一 `{error, path}` 形狀
- [x] 全域 `Exception` handler：log `exception`，回應固定 `Internal server error`
- [x] `RequestLoggingMiddleware`：method／path／status／耗時
- [x] log 同時到 console 與 `logs/app.log`（gitignore）
- [x] objectlist 404 改 `AppException`；`tests/test_w10_errors.py` 通過

## 3. 問 AI 的三個重要問題
- [x] Q1 為什麼 500 不能把 traceback 回給瀏覽器？
- [x] Q2 為什麼還要幫 `HTTPException` 寫 handler，不只做 `AppException`？
- [x] Q3 middleware 記的「耗時」大概從哪量到哪？

### Q1
- Prompt:
未預期例外時，為什麼回應只要固定「Internal server error」，詳細錯誤只寫進 log？
- AI 建議摘要:
traceback／檔名／SQL 可能洩漏結構或密鑰線索，方便攻擊。對使用者只要知道失敗；開發者看 `logs/app.log` 的 `logger.exception`。
- 我驗證的方法:
`test_unhandled_exception_hides_details`：回傳無 `RuntimeError`／secret 字串，status 500。
- 最後我採用 / 修改 / 拒絕了什麼:
採用隱藏細節；拒絕把 exception 字串直接當 JSON error。

### Q2
- Prompt:
專案很多地方仍 `raise HTTPException`，為什麼還要註冊 HTTPException handler？
- AI 建議摘要:
一次改完全部 raise 成本高。用 handler 把既有 HTTPException 轉成與 AppException 相同的 `{error, path}`，格式先統一；新程式可逐步改 `AppException`。
- 我驗證的方法:
未登入打 `/api/auth/me` → 401 且 body 有 `error`／`path`。
- 最後我採用 / 修改 / 拒絕了什麼:
兩種例外並存；objectlist 當 AppException 範例。

### Q3
- Prompt:
請求 logging middleware 的秒數是在量什麼？
- AI 建議摘要:
從進入 middleware、呼叫 `call_next` 前後用 `perf_counter` 差分，大致含路由＋依賴＋DB／業務時間（外層還有 Session 等）。用來找慢請求，不是精準 APM。
- 我驗證的方法:
打 `/api/health` 後 console／`logs/app.log` 出現 `GET /api/health 200 0.xxxs`。
- 最後我採用 / 修改 / 拒絕了什麼:
採用 INFO 記成功請求；例外路徑先 ERROR 再交 exception handler。

## 4. Web Concept of the Week
```text
AppException／HTTPException → {error, path}
未預期 Exception → log stack；對外固定 500 文案
Middleware：METHOD path status duration
```

## 5. Debugging Record
- Problem: 講義範例 `Status_code`／`from FastAPI import` 大小寫不正確
- Fix: 依正式 FastAPI 寫 `status_code`、`fastapi.Request`／`JSONResponse`

## 6. Security Check
- 500 不回 traceback
- `logs/` 不進 git（可能含路徑／查詢訊息）

## 7. Reflection (反思)
W10 是「給人看的錯誤」跟「給維運看的 log」分開。
- 下次: 其餘 router 可逐步改 `AppException`；ValidationError 若要同形狀再加 handler。

---
