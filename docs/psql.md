# FastAPI + PostgreSQL 後端系統開發：12 週實作課程

> 針對已有全端開發與系統架構背景的學習者設計，跳過基礎語法複習，直接進入後端系統的實務建構。每週包含：學習目標、為什麼這樣安排、實作步驟、本週練習、驗收標準。

## 總覽


| 週次  | 主題                                 | 產出                           |
| --- | ---------------------------------- | ---------------------------- |
| W01 | FastAPI 專案架構與基礎 API                | 可執行的 Hello API 專案骨架          |
| W02 | PostgreSQL 安裝與連線                   | 資料庫連線成功、建立第一個 table、加入API    |
| W03 | SQLAlchemy ORM + Alembic Migration | Model 定義與版本化的 schema         |
| W04 | CRUD API 完整實作                      | 一組完整的 RESTful CRUD 端點        |
| W05 | 關聯式設計（一對多、多對多）                     | 多資料表關聯查詢                     |
| W06 | 身份驗證（JWT / OAuth2）                 | 登入、保護路由                      |
| W07 | 測試（pytest）                         | 自動化測試覆蓋 CRUD + Auth          |
| W08 | 非同步與連線池                            | Async ORM 操作、效能觀念            |
| W09 | 進階查詢：分頁、篩選、搜尋                      | Query 參數化的 API               |
| W10 | 錯誤處理、Logging、Middleware            | 具生產等級的錯誤回應與紀錄                |
| W11 | Docker 化                           | docker-compose 一鍵啟動 API + DB |
| W12 | 部署與整合專題                            | 完整可展示的後端專案                   |


---



## W1：FastAPI 專案架構與基礎 API



### 學習目標

理解 FastAPI (Python) 的專案結構慣例，以及它跟 (Node.js) Express.js / Spring Boot 這類框架的對應關係。

### 為什麼這樣安排

自學 REST API 設計，不花時間講「什麼是 API」，而是直接建立你之後 12 週都會沿用的專案骨架，這樣後面每週只需要疊加功能。

### 操作步驟

- install Python Install Manager (Windows Market)

```bash
mkdir api
cd api
py -m venv venv
venv\Scripts\activate      # Windows Powershell, Set-ExecutionPolicy
pip install fastapi uvicorn[standard]
```

實際能跑的:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

deactivate
```

建立專案結構：開始學習與思考自己或團隊習慣的program structures

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   └── models/
│       └── __init__.py
├── requirements.txt
└── venv/
```

`app/main.py`：

```python
from fastapi import FastAPI

app = FastAPI(title="My Backend API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

啟動：

```bash
uvicorn app.main:app --reload
```

打開 `http://127.0.0.1:8888/docs`，這是 FastAPI 自動產生的 Swagger UI（對應你熟悉的 Swagger/OpenAPI 概念，但這裡完全自動產生，不用手寫 YAML）。

### 本週練習

1. 新增一個 `/version` 端點，回傳 `{"version": "0.1.0"}`
2. 用 Pydantic 定義一個 `Item` 模型（含 `name: str`、`price: float`），寫一個 `POST /items` 接收並回傳它
3. 執行 `pip freeze > requirements.txt`，理解這個檔案對應 Node.js 的 `package.json` 扮演什麼角色
4. AI：為 py + fastapi + psql 建立 .gitignore
5. Install Git、建立 github repo，並push and commit

```git
# 1. 建立本機第一個 commit
git add .
git commit -m "W1: FastAPI Test"

# 2. 設定 GitHub 遠端 repository
git remote add origin https://github.com/icsie/api.git

# 3. 設定主分支名稱
git branch -M main

# 4. 發現 GitHub 已有 Initial commit，因此先取得遠端歷史
git fetch origin

# 5. 合併本機與 GitHub 的不同歷史
git merge origin/main --allow-unrelated-histories

# 6. 推送到 GitHub
git push -u origin main
```



### 驗收標準

- [x] `/docs` 能正常開啟並看到自訂端點
- [x] `POST /items` 能正確驗證型別（試著傳錯誤型別，觀察 FastAPI 自動回傳的 422 錯誤）
- [x] 了解建立根目錄的 .gitignore，涵蓋：Python 虛擬環境與快取、pytest、coverage、mypy、ruff 產物、.env 設定檔、FastAPI/Uvicorn log、PostgreSQL 本地資料與備份、VS Code、IDE 與作業系統檔案
- [x] 學會 `.gitignore`：`!` 取消忽略，例如 !.env.example 會保留範例設定檔。
- [x] add .env.example，並commit and push確認出現自github repo。



### 本週筆記

- PowerShell：本機腳本可用 `RemoteSigned`；下載來的 `.ps1` 仍要留意簽章／解除封鎖。
- VS Code：改 PATH（如裝 Git）後須關乾淨再開，終端機才吃得到。
- Git：遠端新建 repo 儘量空白（勿先建 README／LICENSE），第一次 push 較單純。

---



## W2：PostgreSQL 安裝與連線



### 學習目標

在本機建立 PostgreSQL，並讓 Python 程式成功連線。

### 為什麼這樣安排

先確保「資料庫本身活著、連得上」，再進到 ORM 抽象層。這樣之後如果連線出錯，你能分辨是資料庫問題還是程式碼問題。

### 操作步驟

**安裝 PostgreSQL（Windows Admin）**

1. 到官方下載頁安裝 PostgreSQL（建議 16 版以上）
2. 安裝時會要求設定 `postgres` 超級使用者密碼，記下來
3. 建議一併安裝 pgAdmin（GUI 管理工具，對應你熟悉的 DBeaver / TablePlus 概念）

**安裝 PostgreSQL（Windows Users Permission，電腦教室用此法安裝）**

若目前帳號只有一般 `Users` 權限，建議使用 PostgreSQL ZIP 免安裝版。此方式不建立 Windows Service，也不需要寫入 `Program Files`，可安裝在使用者目錄。

1. 下載與作業系統相容的 PostgreSQL Windows ZIP binary。
2. 將 ZIP 解壓縮至使用者目錄，例如：

```text
C:\Users\<你的帳號>\pgsql
```

1. 建立資料目錄：

```powershell
mkdir "$env:USERPROFILE\pgsql-data"
```

1. 初始化資料庫叢集：

```powershell
cd "$env:USERPROFILE\pgsql"

.\bin\initdb.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  -U postgres `
  -A scram-sha-256 `
  -W
```

執行後依提示設定 `postgres` 使用者密碼。

1. 啟動 PostgreSQL。若 `5432` 已被其他服務使用，可使用 `5433`：

```powershell
.\bin\pg_ctl.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  -o "-p 5433" `
  -l "$env:USERPROFILE\pgsql-data\server.log" `
  start
```

1. 連線測試：

```powershell
.\bin\psql.exe `
  -h localhost `
  -p 5433 `
  -U postgres `
  -d postgres
```

1. 在 `psql` 中建立開發用資料庫與使用者：

```sql
CREATE USER dev_user WITH PASSWORD 'your_password';
CREATE DATABASE fastapi_dev OWNER dev_user;
\c fastapi_dev
GRANT ALL ON SCHEMA public TO dev_user;
```

檢查是否成功寫入DB：

```sql
SELECT version(); SELECT current_database(), current_user;
```

結束PSQL DB：

```sql
exit
```

1. 修改 `.env`：

```env
DATABASE_URL=postgresql://dev_user:your_password@localhost:5433/fastapi_dev
```

停止 PostgreSQL：

```powershell
.\bin\pg_ctl.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  stop
```

> ZIP 版本不會自動建立 Windows Service，因此每次使用前需要執行 `pg_ctl start`。若要讓 PostgreSQL 開機自動啟動，通常需要系統管理員協助建立服務。



#### 建立開發用資料庫與使用者

```sql: add file .\psql\createdb.sql
-- 用 psql 或 pgAdmin 執行
CREATE DATABASE fastapi_dev;
CREATE USER dev_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_dev TO dev_user;

\connect fastapi_dev
GRANT USAGE, CREATE ON SCHEMA public TO dev_user; -- public schema建表權限
```

```pwsh: psql 執行
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' `
  -U postgres `
  -d postgres `
  -f .\psql\createdb.sql
```

**Python 端安裝驅動**

```bash
pip install "psycopg[binary]" python-dotenv
```

`.env`（不要進版控，需加入 `.gitignore`）：

```
DATABASE_URL=postgresql://dev_user:your_password@localhost:5432/fastapi_dev
```

測試連線 `app/core/db_test.py`：

```python
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def test_connection():
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    print("連線成功:", conn.info.dbname)
    conn.close()

if __name__ == "__main__":
    test_connection()
```

```pwsh
python .\app\core\db_test.py
```

連線成功: fastapi_dev

### 本週練習

1. 用 `psql` 指令手動建立一個 `notes` table（欄位：`id`, `title`, `content`, `created_at`）；用 `INSERT` 手動塞3筆資料，再用 `SELECT` 查回來
2. New REST api: /note/{id}



### 驗收標準

- [x] Python 程式能成功連上 PostgreSQL
- [x] 能說明為什麼密碼要放在 `.env` 而不是寫死在程式碼裡（對應你熟悉的環境變數管理概念）
- [x] Test API and data format (了解Swagger用法，具備測試API能力)



### 本週筆記（venv／pg_ctl／流程見 `ai.md` W02）

- 可用 VS Code SQLTools 跑 SQL；日常用開發帳號，勿濫用 `postgres` 超管。
- 新建庫後記得對 `public` schema 授權建表。
- 真實密碼只放本機 `.env`；本文件與 Git 只用佔位符。

---



## PostgreSQL 基本操作：流程、原理、區別



### 三角色先分清


| 工具          | 本質               | 類比        |
| ----------- | ---------------- | --------- |
| `pg_ctl`    | 開／關「資料庫伺服器」行程    | 開門／關門     |
| `psql`      | 進門後用文字下 SQL、管理指令 | 進門辦事（終端機） |
| **pgAdmin** | 同一件事的圖形介面        | 進門辦事（視窗）  |


`psql` 和 pgAdmin **都是客戶端**，都要連上已經在跑的伺服器。伺服器沒開，兩者都連不上。

```text
你（客戶端）
  ├─ psql          ──TCP──►  PostgreSQL 伺服器（5433）
  └─ pgAdmin       ──TCP──►       ↑
                              由 pg_ctl start 啟動
```

---



## 日常標準流程（本機 ZIP · 5433）



### 1. 開伺服器（PowerShell，不必進 venv）

```powershell
& "$env:USERPROFILE\pgsql\bin\pg_ctl.exe" `
  -D "$env:USERPROFILE\pgsql-data" `
  -o "-p 5433" `
  -l "$env:USERPROFILE\pgsql-data\server.log" `
  start
```

看狀態：

```powershell
& "$env:USERPROFILE\pgsql\bin\pg_ctl.exe" -D "$env:USERPROFILE\pgsql-data" status
```



### 2A. 用終端機辦事（課程主練）

```powershell
cd $env:USERPROFILE\pgsql
.\bin\psql.exe -h 127.0.0.1 -p 5433 -U 你的帳號 -d fastapi_dev -W
```

進去後常見指令：

```sql
SELECT current_user, current_database();
\dt                          -- 列出資料表
SELECT * FROM notes;
\q                           -- 離開（回到 PowerShell）
```



### 2B. 用圖形介面辦事（方便看）

pgAdmin → 連 `localhost:5433`、你的帳號、`fastapi_dev` → **Query Tool** 打同一段 SQL。

### 3. 測 FastAPI（要 venv / run.bat）

資料庫開著之後：

```powershell
cd C:\Users\admin\code\fastapi-backend
.\run.bat
```

API 用 `.env` 的 `DATABASE_URL` 連同一台 5433。

### 4. 用完可關伺服器（不強制）

```powershell
& "$env:USERPROFILE\pgsql\bin\pg_ctl.exe" -D "$env:USERPROFILE\pgsql-data" stop
```

關了之後 `psql`／pgAdmin／`/api/notes` 都會連不上。

---



## 原理（為什麼要這樣）

1. **伺服器常駐**
  `pg_ctl start` 把 `postgres.exe` 跑起來，聽某個埠（你是 5433）。資料存在 `pgsql-data` 目錄，不是存在 `psql` 裡。
2. **連線＝帳號 + 庫 + 認證**
  客戶端帶：主機、埠、使用者、密碼、要進哪個 database。  
   `pg_hba.conf` 決定「要不要密碼」（你現在是 `scram-sha-256`）。
3. **SQL 在「已連上的那個庫」執行**
  `-d fastapi_dev` 或 `\c fastapi_dev` 之後，`SELECT * FROM notes` 才找得到表。連錯庫會覺得「表不見了」。
4. **FastAPI 也是客戶端**
  和 `psql` 一樣走網路連 5433；差在程式用 `psycopg`，連線字串在 `.env`。

---



## 區別對照


|         | `pg_ctl`          | `psql`       | pgAdmin |
| ------- | ----------------- | ------------ | ------- |
| 開／關伺服器  | ✓                 | ✗            | ✗（連現成的） |
| 下 SQL   | �／關伺服器            | ✓            | ✗       |
| 下 SQL   | ✗                 | ✓            | ✓       |
| 要密碼     | 通常不用              | 連線時要         | 登錄時要    |
| 要 venv  | 否                 | 否            | 否       |
| 課程文件多寫誰 | start／stop／status | 建表、INSERT、查詢 | 較少，當輔助  |



|       | `psql`       | FastAPI `/api/notes`    |
| ----- | ------------ | ----------------------- |
| 誰連 DB | 你手動          | 程式自動                    |
| 帳密從哪來 | 指令列 `-U`     | `.env` 的 `DATABASE_URL` |
| 用途    | 管理、除錯、練習 SQL | 給網頁／Swagger 用           |



|                  | 埠 5433（ZIP） | 埠 5432（官方） |
| ---------------- | ----------- | ---------- |
| 你的課程 `.env`      | ✓ 用這個       | 另一套，別混     |
| pgAdmin 要選對 Port | `5433`      | `5432`     |


---



## 最短口訣

```text
pg_ctl start
  → psql 或 pgAdmin 連進去下 SQL
  → （測 API）run.bat
  → psql 用 \q 離開；不需要時再 pg_ctl stop
```

記住：**先開門（pg_ctl），再進門（psql／pgAdmin）；進錯門（錯埠／錯庫／錯帳號）就什麼都找不到。**

## W03：Run FastAPI as Web App and API



### 學習目標

用FastAPI做為http server，同時服務web app and api。

root

> Add run.bat to run fastapi with local_IP:7777

app\main.py

> Make fastapi to be a http server with a folder as the root.

- Set public_directory to your webui
- 仔細測試觀察是否有問題？
  > Make all api paths correspond to /api/
- 仔細測試觀察是否有問題？
  > #sym:StaticFiles: restrict public access to .html and .css only.
- 注意Browser HTTP cache問題
  > 另開無痕測試就好了，why? 以後如何注意此問題
- F12 > Network > Disable Cache



### 驗收標準

- [x] local IP可存取
- [x] 上課與TA設定 [https://demo.wke.csie.ncnu.edu.tw/](https://demo.wke.csie.ncnu.edu.tw/) 可存取
- [x] 盡量測試，列出問題討論



### 本週筆記（IIS／路由／Swagger／尾斜線／快取見 `ai.md` W03）

依 `main.py` 組裝順序，只記文件沒寫過的實作細節：

1. `**public_directory**`：`Path(__file__).resolve().parents[2] / "webui-lab"`——從 `app/main.py` 往上兩層到專案上層，再進前端資料夾。
2. `**Item`（Pydantic）**：自動驗證 body；缺欄／型別錯 → `422`。目前 `POST /api/items` 只驗證後原樣回傳，**尚未寫入 DB**。
3. `**app.include_router(api_router)**`：沒這行，上面的 `/api/*` 函式不會掛上網址。
4. **先** `serve_index`**（**`/`**）再** `mount("/", …)`：較精確的路由先註冊；剩下的 html／css 才交給靜態掛載。
5. **靜態限制**：只允許 `.html`／`.css`（老師要求）；其它副檔名回 `404`。

---



## W04：CRUD API 完整實作



### RESTful API

RESTful API 是一種以「資源（resource）」為中心設計 HTTP API 的方式。每一種資源都有固定的 URL，例如 `/notes` 代表筆記集合，`/notes/{id}` 代表某一筆筆記；用不同的 HTTP method 表達對資源的操作，而不是為每個動作建立不同的動詞型 URL。

CRUD 分別代表 **Create（新增）**、**Read（查詢）**、**Update（更新）**、**Delete（刪除）**。以下以 `notes` 資源為例：


| CRUD     | HTTP method | 範例路徑          | 使用時機                | 請求／回應範例                                                                     |
| -------- | ----------- | ------------- | ------------------- | --------------------------------------------------------------------------- |
| Create   | `POST`      | `/notes`      | 建立一筆新資源，由伺服器產生 `id` | 請求：`{"title": "學習 REST", "content": "理解 CRUD"}` 回應：`201 Created` 與建立後的 note |
| Read（列表） | `GET`       | `/notes`      | 取得資源集合，可搭配分頁、篩選或搜尋  | 回應：`200 OK` 與 notes 陣列                                                      |
| Read（單筆） | `GET`       | `/notes/{id}` | 取得指定 `id` 的資源       | 回應：`200 OK` 與單筆 note；不存在時回傳 `404 Not Found`                                 |
| Update   | `PUT`       | `/notes/{id}` | 以完整資料取代指定資源         | 請求：`{"title": "更新標題", "content": "更新內容"}` 回應：`200 OK` 與更新後的 note            |
| Delete   | `DELETE`    | `/notes/{id}` | 刪除指定資源              | 回應：`204 No Content`；不存在時回傳 `404 Not Found`                                  |


設計 API 時，路徑通常使用名詞而不是動詞，例如使用 `POST /notes`，而不是 `/createNote`。同一個 HTTP method 與 URL 應具有一致且可預期的語意，讓前端、其他服務與 API 文件都容易理解與使用。

### 學習目標

串接API與資料庫，完成一組完整 RESTful CRUD。

### 為什麼這樣安排

這是第一個「垂直切片」（vertical slice）——從 HTTP 請求到資料庫的完整路徑打通，之後每一週都是在這個路徑上疊加功能，而不是零散學習。

### AI coding

> 針對/api/note 加入REST CRUD功能 (需對應慣用HTTP Method)

- 仔細觀察修改的程式碼，另開瀏覽器詢問AI以求理解
- 撰寫學習心得



### 人工操作步驟



#### 分層設計理念：routers → schemas → repositories → core

將 API 拆成不同層次，是為了讓每個檔案只負責一種工作，降低修改時彼此影響的範圍。一次請求大致會依照以下流程處理：

1. **Routers（路由層）**：決定 API 的 URL、HTTP method 與回應狀態，接收請求後呼叫下一層，不直接撰寫大量 SQL 或資料庫連線細節。
2. **Schemas（資料格式層）**：使用 Pydantic 定義請求與回應格式，負責型別驗證、欄位限制，以及避免把資料庫內部欄位直接暴露給前端。
3. **Repositories（資料存取層）**：集中處理 SQL 與資料庫 CRUD，讓 Router 不需要知道資料表查詢的細節。
4. **Core（共用基礎設施層）**：提供資料庫連線、設定、驗證或其他全域共用功能；例如 `core/db.py` 管理 PostgreSQL 連線。

因此，實際的責任關係可以理解為：

```text
HTTP request
    → routers/notes.py       路由與流程控制
    → schemas/notes.py        請求資料驗證
    → repositories/notes.py  SQL 與資料存取
    → core/db.py              PostgreSQL 連線
    → HTTP response
```

相關檔案的使用方式如下：


| 元件                     | 目前專案檔案                      | 主要用途                                   |
| ---------------------- | --------------------------- | -------------------------------------- |
| Router                 | `app/routers/notes.py`      | 定義 `/api/notes` 等端點，處理 HTTP 請求與回應      |
| Schema                 | `app/schemas/notes.py`      | 定義 `NoteCreate`、`NoteResponse` 等輸入輸出模型 |
| Repository             | `app/repositories/notes.py` | 封裝 notes 的 SQL 查詢、新增、更新與刪除             |
| Core                   | `app/core/db.py`            | 建立與管理 PostgreSQL 資料庫連線                 |
| Core                   | `app/core/static_files.py`  | 集中處理前端靜態檔案的提供方式                        |
| Application entrypoint | `app/main.py`               | 建立 FastAPI app、註冊 Router 與設定整體服務       |


這種分層方式的重點不是檔案越多越好，而是讓變更容易定位：API 路徑改動主要看 Router，資料格式改動看 Schema，SQL 改動看 Repository，資料庫連線設定則集中在 Core。

#### ORM 技術概念

ORM（Object-Relational Mapping，物件關聯式對映）是把 Python 物件與關聯式資料庫的資料表對應起來的技術。開發者可以操作 `Note` 這類 Python model，ORM 再將操作轉換成 PostgreSQL 能理解的 SQL。

簡單對照如下：


| ORM 概念           | Python / SQLAlchemy 範例       | 資料庫概念                  |
| ---------------- | ---------------------------- | ---------------------- |
| Model class      | `class Note`                 | `notes` 資料表            |
| Object attribute | `note.title`                 | `title` 欄位             |
| Object instance  | `note = Note(...)`           | 一筆資料（row）              |
| Query            | `db.query(Note).filter(...)` | `SELECT ... WHERE ...` |
| `db.add()`       | 將物件加入 Session                | 準備新增一筆資料               |
| `db.commit()`    | 提交 Session 的變更               | 真正寫入資料庫                |


例如，以下 ORM 查詢：

```python
note = db.query(Note).filter(Note.id == note_id).first()
```

概念上相當於：

```sql
SELECT * FROM notes WHERE id = :note_id LIMIT 1;
```

其中 `db` 通常是 SQLAlchemy 的 `Session`。Session 可以理解成一次資料庫操作的工作範圍，負責追蹤物件變更、送出查詢，以及透過 `commit()` 確認交易。若發生錯誤，也可以使用 `rollback()` 撤銷尚未提交的變更。

使用 ORM 的好處是可以用 Python model 與型別來表達資料操作，減少手寫 SQL 的數量，並集中處理交易與資料庫連線；但仍然需要理解 SQL，因為 ORM 最後仍會產生 SQL，複雜查詢也可能需要直接使用 SQLAlchemy 的查詢語法。

本節為了讓 CRUD 流程集中，先在 Router 中直接示範 ORM 操作。實際專案可將 `db.query()`、`db.add()` 等資料庫操作移到 `app/repositories/notes.py`，讓 Router 只負責接收請求、呼叫 Repository 與回傳結果。

`app/schemas/note.py`（Pydantic schema，區分「API 輸入輸出」與「資料庫 model」是重要慣例）：

```python
# Schema 只描述 API 收到與回傳的資料格式，不負責執行 SQL。
# import 是匯入其他套件或模組，讓目前檔案可以使用其中的類別與函式。
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# POST /notes 使用的請求格式；content 可省略。
# class 用來定義一個可重複使用的資料結構或物件類別。
class NoteCreate(BaseModel):
    # 冒號後的 str 是型別註記，表示 title 預期是一段文字。
    title: str
    # Optional[str] 表示可以是文字或 None；= None 表示預設值是 None。
    content: Optional[str] = None

# API 回應格式；不直接暴露資料庫 model 給前端。
class NoteResponse(BaseModel):
    # Pydantic 會依照這些型別註記檢查與轉換資料。
    id: int
    title: str
    content: Optional[str]
    created_at: datetime

    # 允許 Pydantic 從 ORM model 的屬性建立回應資料。
    # 內嵌 class Config 是設定這個 Pydantic model 行為的舊版寫法。
    class Config:
        # ORM 物件像 note.title；一般字典則像 {"title": "學習 REST"}。
        # True 允許 Pydantic 讀取 ORM 物件的屬性，轉成 NoteResponse。
        # 若沒有這項設定，通常只能從字典鍵值建立，例如 NoteResponse(**data)。
        from_attributes = True
```

`app/api/notes.py`：

```python
# Router 負責 HTTP 路由與流程控制；資料庫細節可再委派給 repository。
# APIRouter 是 FastAPI 用來集中管理一組相關 API 路由的類別。
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse

# 同一組 notes 資源共用路徑前綴與 OpenAPI 分類。
# 關鍵字參數使用 name=value，讓設定的意義比位置順序更清楚。
router = APIRouter(prefix="/notes", tags=["notes"])

# Create：先由 NoteCreate 驗證請求，再建立資料庫 model。
# @ 是 decorator 語法：把函式註冊成指定 HTTP method 與路徑的 API endpoint。
# response_model 會驗證並限制回傳給前端的欄位格式。
@router.post("/", response_model=NoteResponse)
# note: NoteCreate 是請求 body，db 由 FastAPI 依賴注入，不需手動建立連線。
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    # ** 會把字典的 key/value 展開成函式或類別建構子的關鍵字參數。
    db_note = Note(**note.model_dump())
    # model_dump() 將 Pydantic model 轉成一般 Python 字典。
    db.add(db_note)
    # add、commit、refresh 是 ORM 常見的新增、提交、重新讀取資料流程。
    db.commit()
    db.refresh(db_note)
    return db_note

# Read：回傳所有 notes，response_model 會統一輸出格式。
# list[NoteResponse] 表示回應是一個由 NoteResponse 組成的列表。
@router.get("/", response_model=list[NoteResponse])
# Depends(get_db) 表示呼叫 endpoint 時，由 FastAPI 執行 get_db 並傳入結果。
def list_notes(db: Session = Depends(get_db)):
    # .all() 將查詢結果全部取回；資料量大時應搭配分頁。
    return db.query(Note).all()

# Read：依照 note_id 查詢單筆資源。
@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    # .filter() 加入查詢條件，== 是建立 SQL 條件，不是立即比較 Python 值。
    note = db.query(Note).filter(Note.id == note_id).first()
    # if not 可檢查查詢結果是否為 None 或其他「沒有資料」的狀態。
    if not note:
        # HTTPException 會讓 FastAPI 回傳指定的 HTTP 錯誤狀態與訊息。
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Update：以 NoteCreate 的完整資料更新指定資源。
@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # for 逐一處理字典內容；key 是欄位名稱，value 是要寫入的新值。
    for key, value in note_data.model_dump().items():
        # setattr(obj, name, value) 依欄位名稱動態設定物件屬性。
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

# Delete：找不到資源時回傳 404，避免讓呼叫端誤以為刪除成功。
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # delete 標記 ORM 物件待刪除，commit 後才會真正寫入資料庫。
    db.delete(note)
    db.commit()
    # return 的字典會被 FastAPI 自動序列化成 JSON 回應。
    return {"detail": "deleted"}
```

在 `app/main.py` 註冊路由：

```python
from app.api import notes
app.include_router(notes.router)
```



### 本週練習

1. 為 `User` 或個人專案會用到的資料表，也做一組完整 CRUD
2. 思考並實作：`DELETE` 時如果 note 不存在，回傳的狀態碼與錯誤訊息是否符合 REST 慣例
3. 用 `/docs` 的 Swagger UI 手動測試所有端點



### 驗收標準

- [x] 五個 CRUD 端點全部正常運作
- [x] 錯誤情境（找不到資源）回傳正確的 HTTP 狀態碼



### 學習心得

- 路徑用名詞，是資源名稱、動作用 HTTP 方法，上傳一個檔案也是用 POST。。
- 找不到回 404，新增 201，DELETE 成功 204，PUT更新成功也是 200，id 不存在是 404，body 少 title 是 422。
- 上課講 : 402 PAYMENT IS REQUIREMENT。
- 職責分成 router、schema、repository、`core/db.py`，細節見 `docs/architecture.md`。
- 這週沿用 `psycopg`，沒用文件後半的 SQLAlchemy；測 notes 前要先啟動 5433 上的 PostgreSQL，否則 Swagger 會一直轉。

---



## W05：關聯式設計：view {#DbView}



### 學習目標

雖然用 SQLAlchemy 的 relationship 可以處理跨表關聯，但大量API需求可以在後端DB處理即可。例如：用 `create view` 對應大量SQL JOIN查詢，降低過多SQL寫在Python codes的需求。

SQLAlchemy relationship 跨表關聯範例 (**不須實作練習，僅供複雜度參考**)

`app/models/note.py`（加上外鍵與關聯）：

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Note(Base):
    __Tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    owner_id = Column(Integer, ForeignKey("Members.id"))
    owner = relationship("Member", back_populates="notes")
```

`app/models/Member.py`：

```python
class Member(Base):
    __Tablename__ = "Members"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    notes = relationship("Note", back_populates="owner")
```

多對多需要中介表（association Table）：

```python
from sqlalchemy import Table

note_Tags = Table(
    "note_Tags", Base.meTadaTa,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("Tag_id", ForeignKey("Tags.id"), primary_key=True),
)

class Tag(Base):
    __Tablename__ = "Tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    notes = relationship("Note", secondary=note_Tags, back_populates="Tags")
```

執行 `alembic revision --autogenerate` 產生對應 migration。

### N+1 問題示範

```python
# 有問題的寫法：每個 note 都額外查一次 owner（N+1）
notes = db.query(Note).all()
for note in notes:
    print(note.owner.email)  # 每次都觸發一次 SQL

# 正確寫法：用 joinedload 一次拿完
from sqlalchemy.orm import joinedload
notes = db.query(Note).options(joinedload(Note.owner)).all()
```

#view 一次解決，不需考慮此問題

## Database View

- 先了解Moodle教材TravelTest.sql的tables: Class, Inheritance, CO, Object
- AI coding改MSSQL為PSQL寫法
- 建立function用於跨資料表於單一Transaction (Tx) 內完成資料新增
- 善用 `view` 方便對應API需求



### mssql to psql改寫

> TravelTest.sql改寫psql於academic.sql。都要判斷DB或table是否存在才建立。
> 命名：since -> create_at; lastmodifydt -> update_at

```sql
\if :{?DBName}
\else
\set DBName fastapi_dev
\endif

SELECT format('CREATE DATABASE %I', :'DBName')
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = :'DBName'
)
\gexec

\connect :DBName

CREATE TABLE IF NOT EXISTS class (
    cid integer NOT NULL,
    type smallint,
    name varchar(100),
    des varchar(1000),
    idpath varchar(100),
    namepath varchar(200),
    create_at timestamp without time zone,
    update_at timestamp without time zone,
    nobject integer,
    crank smallint,
    orank smallint,
    code varchar(255),
    keywords varchar(255),
    nlevel smallint,
    imgid smallint,
    nclicktrue integer NOT NULL DEFAULT 0,
    nclick integer NOT NULL DEFAULT 0,
    property smallint NOT NULL DEFAULT 0,
    CONSTRAINT pk_class PRIMARY KEY (cid),
    CONSTRAINT uq_idpath UNIQUE (idpath),
    CONSTRAINT uq_namepath UNIQUE (namepath)
);

INSERT INTO class (cid, name, idpath, namepath)
VALUES (0, '首頁', '0', '首頁')
ON CONFLICT DO NOTHING;

ALTER TABLE class
ALTER COLUMN cid    -- Set the cid to be an identity column
ADD GENERATED BY DEFAULT AS IDENTITY;

CREATE TABLE IF NOT EXISTS inheritance (
    pcid integer NOT NULL,
    ccid integer NOT NULL,
    rank smallint,
    mg smallint,
    CONSTRAINT pk_inheritance PRIMARY KEY (pcid, ccid),
    CONSTRAINT fk_inheritance_pcid FOREIGN KEY (pcid) REFERENCES class (cid),
    CONSTRAINT fk_inheritance_ccid FOREIGN KEY (ccid) REFERENCES class (cid)
);

CREATE TABLE IF NOT EXISTS object (
    oid integer NOT NULL,
    title varchar(200),
    class varchar(50),
    des varchar(1000),
    address varchar(400),
    telephone varchar(50),
    sourceurl varchar(400),
    nclick integer NOT NULL DEFAULT 0,
    CONSTRAINT pk_object PRIMARY KEY (oid)
);
ALTER TABLE object
ALTER COLUMN oid    -- Set the oid to be an identity column
ADD GENERATED BY DEFAULT AS IDENTITY;

CREATE TABLE IF NOT EXISTS co (
    cid integer NOT NULL,
    oid integer NOT NULL,
    rank smallint,
    mg smallint,
    CONSTRAINT pk_co PRIMARY KEY (cid, oid),
    CONSTRAINT fk_co_cid FOREIGN KEY (cid) REFERENCES class (cid),
    CONSTRAINT fk_co_oid FOREIGN KEY (oid) REFERENCES object (oid)
);

```



### academic.sql: add function

在目錄下新增子目錄：

> fun insertClass(pcid, pname, cname): 
>
> 1. match class where pcid, cname then add class(cname) and get cid as ccid
> 2. insert Inheritance(pcid, ccid)
> 3. update namepath and idpath to the class(ccid)

```sql
CREATE OR REPLACE FUNCTION insertClass(pcid integer, pname varchar, cname varchar)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
    v_ccid integer;
    parent_idpath varchar(100);
BEGIN
    if exists (select 1 from class where cid = $1) = false then
        RAISE EXCEPTION 'Parent class with cid % does not exist', pcid;
    end if;
    if exists (select 1 from class where cid = $1 and name = $2) = false then
        RAISE EXCEPTION 'Class with cid %, name % does not exist', $1, $2;
    end if;

    SELECT c.cid
    INTO v_ccid
    FROM inheritance AS i, class AS c
    WHERE i.pcid = $1   -- parent cid 
      AND c.cid = i.ccid
      AND c.name = $3   -- child class name => if exists, return the existing cid
    ORDER BY c.cid
    LIMIT 1;
    -- new child class, insert it with the given name and return the new cid
    IF v_ccid IS NULL THEN  
        INSERT INTO class (name)
        VALUES ($3)
        RETURNING cid INTO v_ccid;
    END IF;
    -- Insert into inheritance table to establish the parent-child relationship
    INSERT INTO inheritance (pcid, ccid)
    VALUES ($1, v_ccid)
    ON CONFLICT ON CONSTRAINT pk_inheritance DO NOTHING;

    SELECT idpath   -- Get the idpath of the parent class
    INTO parent_idpath
    FROM class
    WHERE cid = $1;

    UPDATE class
    SET namepath = concat_ws('/', NULLIF($2, ''), $3),
        idpath = concat_ws('/', NULLIF(parent_idpath, ''), v_ccid::varchar)
    WHERE cid = v_ccid;

    RETURN v_ccid;
END;
$$;
```



### Test and Add data

```sql
SELECT insertClass(0, '首頁', 'shlin');
SELECT * from class;    -- cid = 4
SELECT insertClass(4, 'shlin', '主控台');
SELECT insertClass(4, 'shlin', '授課');
SELECT insertClass(4, 'shlin', '導師');
SELECT insertClass(4, 'shlin', '校務');
SELECT insertClass(4, 'shlin', '個人設定');
SELECT * from class;    -- cid = 5 ~ 9
SELECT insertClass(5, '主控台', '個人總覽');
SELECT insertClass(5, '主控台', '待辦事項');
SELECT insertClass(5, '主控台', '教務行事曆');
SELECT insertClass(5, '主控台', '通知中心');
SELECT insertClass(6, '授課', '開課前');
SELECT insertClass(6, '授課', '上課中');
SELECT insertClass(6, '授課', '開課記錄');
SELECT insertClass(7, '導師', '導師公告');
SELECT insertClass(7, '導師', '導師規章');
SELECT insertClass(8, '校務', '教務公告');
SELECT insertClass(8, '校務', '教務規章');
SELECT insertClass(8, '校務', '開課查詢');
SELECT insertClass(8, '校務', '服務資訊');
SELECT insertClass(9, '個人設定', '基本資料');
SELECT insertClass(9, '個人設定', '通知設定');
SELECT insertClass(9, '個人設定', '申請紀錄');
SELECT insertClass(9, '個人設定', '問題回報');
SELECT insertClass(9, '個人設定', '登入紀錄');
SELECT * from class;    -- cid = 5 ~ 9
```



### RESE API for sidebar

> I've created view [vd_subclass] with pgsql. Add /api/subclass/pcid/{id} to GET data from the view where pcid = {id}

```sql
CREATE OR REPLACE VIEW vd_subclass AS
SELECT p.cid as pcid, p.name as parent_name, c.cid as cid, c.name as child_name
FROM class p, inheritance i, class c
WHERE p.cid = i.pcid AND c.cid = i.ccid;
SELECT * FROM vd_subclass where pcid = 4;
SELECT * FROM vd_subclass where pcid = 9;

GRANT SELECT ON vd_subclass TO dev_user; -- API最小授權原則
```

要記得授權，讓帳號可以讀view。

- **API最小授權原則**



### 本週練習 (對應自己Project需求開始實作)

1. 完成Sidebar對應TravelTest DB的vd_subclass API需求
2. vd_objectlist：click 鄉鎮市區，取得景點列表
3. vd_object：取得景點詳細資訊



### 驗收標準

- [x] REST API測試
- [x] API最小授權原則

---



## W06：身份驗證（JWT / OAuth2） {#OAuth}



### 學習目標

實作註冊、登入、JWT 簽發，以及保護需要登入才能存取的端點。

完成本週後，學生應該能：

1. 說明 Authentication（身份驗證）與 Authorization（授權）的差異。
2. 說明 OAuth 2.0、OpenID Connect（OIDC）、SSO、JWT 彼此的關係。
3. 使用 Google OIDC 完成 SSO login。
4. 將第一次登入的使用者建立到 PostgreSQL `members` table；再次登入則更新資料，不重複新增。
5. 由自己的 FastAPI backend 簽發「本系統的 JWT」。
6. 使用 JWT 保護需要登入才能存取的 endpoint。
7. 說明 JWT 放在 `localStorage`、`sessionStorage`、HttpOnly cookie、memory 的風險差異。
8. 能回答：JWT 被竄改、過期、帳號被停用、cookie 被刪除時，系統會發生什麼。
9. 使用 AI 協助設計、實作、debug，但能自己畫出並解釋完整 authentication flow。

---



### Authentication vs Authorization

Authentication API

> 「你是誰？」

例如：

- Google 確認這個人真的登入了某個 Google Account。
- FastAPI 根據 JWT 確認 request 對應哪一個 member。

Authorization API

> 「你可以做什麼？」
> 例如：

- member 可以看自己的資料 (e.g. google calendar)。
- 此member權限還是local控管，僅作用於local services，就此與Google無關了。



### 先從 OIDC 登入，再理解 OAuth 2.0 授權

本週建議不要一開始就從 OAuth 2.0 規格談起，而是先從學生最熟悉的情境開始：

> **使用 Google 帳號登入FastAPI網站**

這時我們首先要解決的問題是：

```text
「這個使用者是誰？」
```

這屬於：

```text
Authentication
      ↓
OpenID Connect (OIDC)
```

等登入完成後，再加入第二個需求：

> **登入後，使用者希望讓我們的 FastAPI 系統讀取他的 Google Calendar。**

這時問題就變成：

```text
「這個使用者允許我們的系統做什麼？」
```

這屬於：

```text
Authorization
      ↓
OAuth 2.0
```

因此本課程採用以下學習順序：

```text
先登入
  ↓
OIDC
「你是誰？」

再取得額外權限
  ↓
OAuth 2.0
「你允許我做什麼？」
```

但要注意：

> **技術上 OIDC 是建立在 OAuth 2.0 之上的 identity layer。**

所以這裡只是為了教學理解，先從 OIDC 的登入情境開始。

---



## Case 1：使用 Google 帳號登入 FastAPI

使用者進入我們的網站：

```text
[Browser]
    |
    | Sign in with Google
    v
[FastAPI]
    |
    | redirect
    v
[Google]
    |
    | 驗證 Google Account
    v
[FastAPI]
```

FastAPI希望知道：

```text
這個人是誰？
```

因此要求：

```text
openid
email
profile
```

Google完成身份驗證後，我們可能取得：

```text
sub
email
email_verified
name
picture
```

例如：

```json
{
  "sub": "123456789",
  "email": "amy@gmail.com",
  "email_verified": true,
  "name": "Amy",
  "picture": "https://..."
}
```

FastAPI接著可以：

```text
Google OIDC
    ↓
確認登入者身份
    ↓
取得 sub / email / name
    ↓
查詢 PostgreSQL members
    ↓
第一次登入 → INSERT member
再次登入   → UPDATE member
    ↓
FastAPI 簽發自己的 App JWT
```

這一段的核心是：

```text
Authentication

「這個登入者是誰？」
```

---



### Google Cloud Console

- GMail > 認證信用卡才能開發
- Create Project > search "oauth"
- Google Auth Platform > 用戶端 > Input data
- Add URI: [https://demo.wke.csie.ncnu.edu.tw](https://demo.wke.csie.ncnu.edu.tw)
- Add Redirect URI: [https://demo.wke.csie.ncnu.edu.tw/s115999999/api/auth/google/callback](https://demo.wke.csie.ncnu.edu.tw/s115999999/api/auth/google/callback)



### Web UI

> Header [(王) 王老師] 我要改成[登入]，click以gmail登入，登入後根據gmail資料顯示。API部分先保留，我會後端寫FastAPI串接。

- `GET api/auth/google/login`: begin Google OAuth and redirect the browser.
- `GET api/auth/me`: return the signed-in profile as JSON, for example `{ "name": "王老師", "email": "teacher@example.com", "picture": "https://..." }`.
- Return `401 Unauthorized` from `api/auth/me` when the visitor is not signed in. The frontend then keeps the sign-in link visible.

The frontend uses a same-origin session (`credentials: "same-origin"`). The backend must validate the Google identity and `email_verified` server-side, then manage the session with secure cookie attributes such as `HttpOnly`, `Secure`, and an appropriate `SameSite` policy. Do not put Google client secrets in browser code.

> click icon: pull down dialoug with two functions: Settings and Logout

```js
async function logout() {
    if (!window.confirm("確定要登出嗎？")) {
        return;
    }

    logoutButton.disabled = true;
    try {
        const response = await fetch(new URL("auth/logout", API_PATH), {
            method: "POST",
            credentials: "same-origin"
        });
        if (!response.ok) {
            throw new Error(`登出失敗：${response.status}`);
        }
        window.location.reload();
    } catch (error) {
        logoutButton.disabled = false;
        console.error("無法登出", error);
        window.alert("登出失敗，稍後再試");
    }
}
```



### API and DB

```prompt
加入gmail登入的API功能，我前端已經寫好，完成對應的：
GET api/auth/google/login
GET api/auth/me
並於 ./psql/createtables.sql加入member table，可以記錄取地的gmail資訊，並透過JWT配合後端DB紀錄，於後續requests都可以順利完成
```

看懂修改的程式碼，並經過幾次對話修改。

```prompt
整理此對話的重要修改檔案與對應codes於oauth.md，並說明其技術觀念與細節。
debug過程也隨後詳實記錄討論
```



### README.md / Google Login

Google Developer:

- Google Cloud Console > GMail登入
- Try for feee: 還是要走完信用卡認證過程
- Create Project > the Project > Search "oauth"
- 建立OAuth用戶端 > 用戶端 > 網頁應用程式 > name 
- 新增URI (for CORS): [https://demo.wke.csie.ncnu.edu.tw](https://demo.wke.csie.ncnu.edu.tw)
- 新增redirect URI: [https://demo.wke.csie.ncnu.edu.tw/s115999999/api/auth/google/callback](https://demo.wke.csie.ncnu.edu.tw/s115999999/api/auth/google/callback)
- Save

Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`,
`JWT_SECRET_KEY`, and `SESSION_SECRET_KEY` in `.env`. Register the exact value of
`GOOGLE_REDIRECT_URI` as an authorized redirect URI in Google Cloud Console.
For local HTTP development, set `AUTH_COOKIE_SECURE=false`; use `true` behind
HTTPS in production. Set `AUTH_SUCCESS_REDIRECT_URL` to the frontend URL after
login (including `/s115999999/` when deployed under that path).


| Method | Path                        | Behavior                                                             |
| ------ | --------------------------- | -------------------------------------------------------------------- |
| `GET`  | `/api/auth/google/login`    | Redirect to Google sign-in                                           |
| `GET`  | `/api/auth/google/callback` | OAuth callback; persists the member and sets an HttpOnly JWT cookie  |
| `GET`  | `/api/auth/me`              | Return `name`, `email`, and `picture`; returns `401` when signed out |


- The callback is handled server-side. 
- The JWT is sent as a same-origin cookie by the browser; API clients may alternatively send it as `Authorization: Bearer`.
- Notes and **subclass** endpoints require a valid JWT whose member still exists in
the database.



### Google OAuth / JWT 登入紀錄

本文整理目前 FastAPI 專案的 Google 登入流程、主要程式碼、PostgreSQL schema、部署設定與本次對話中的除錯結果。密碼、OAuth client secret、JWT secret 等值一律不記錄在本文。

## 目前狀態摘要

- 前端進入點：`GET /api/auth/google/login`。
- 正式 Google callback：`GET /api/auth/google/callback`。Google Cloud Console 與 `GOOGLE_REDIRECT_URI` 必須逐字相同；目前使用公開 HTTPS host 與 `/s115999999` 部署前綴，路徑尾端**不加斜線**。
- callback 別名仍存在：`/api/auth/callback`、`/api/auth/callback/`。正式設定仍建議統一使用上面的 `/google/callback` 路徑。
- 登入成功後，後端以 HttpOnly cookie 傳 JWT；`GET /api/auth/me` 回傳登入者資料。
- Notes 與 subclass 路由要求已驗證 JWT，health/version 等公開路由不受影響。
- DB 連線及 `member` 表曾確認存在，但當時 API 使用的 `dev_user` 對 table 和 identity sequence 沒有權限。最新 SQL 已加入 GRANT；需以具備授權權限的 DB role 執行後才會生效。



### 程式碼分工


| 檔案                                                       | 責任與重要程式碼                                                                                                                                                                                                                        |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [app/main.py](app/main.py)                               | 建立 FastAPI app，設定 `root_path="/s115999999"`，掛載 `SessionMiddleware`，將 auth router 加到 `/api` router。OAuth state 存在短效 session cookie；靜態檔案最後才 mount，避免攔截 API。                                                                       |
| [app/routers/auth.py](app/routers/auth.py)               | Authlib 註冊 Google OpenID Connect metadata 及 `openid email profile` scope。`google_login()` 轉址到 Google；`google_callback()` 驗證授權回應、檢查 `sub/email/email_verified`、upsert member、簽發 JWT cookie；`read_current_member()` 提供前端 profile。 |
| [app/core/security.py](app/core/security.py)             | 建立 HS256 JWT，驗證 cookie 或 Bearer token 的簽章、issuer、必要 claims 與期限，再以 `sub` 作 member id。先驗 JWT、後取 DB，確保未登入請求可以直接得到 401。                                                                                                             |
| [app/repositories/member.py](app/repositories/member.py) | 使用參數化 SQL 將 Google profile 寫入 `member`；`google_sub` 衝突時更新 profile。另依 JWT member id 查詢仍存在且已驗證的 member。                                                                                                                           |
| [app/routers/notes.py](app/routers/notes.py)             | router 層級加入 `Depends(get_current_member)`，保護整組 notes API。                                                                                                                                                                       |
| [app/routers/subclass.py](app/routers/subclass.py)       | router 層級加入同一個 member dependency，保護 subclass API。                                                                                                                                                                               |
| [app/core/db.py](app/core/db.py)                         | 由 `DATABASE_URL` 建立 psycopg connection，FastAPI request 結束時關閉 connection。                                                                                                                                                        |
| [psql/createtables.sql](psql/createtables.sql)           | 定義 `member` 表及 `dev_user` 的 table/identity sequence 權限。腳本也會刪除並重建 notes，請先修復檔尾未完成 SQL，並避免在有 notes 資料的正式 DB 執行整份腳本。                                                                                                               |
| [requirements.txt](requirements.txt)                     | 登入依賴包含 Authlib、PyJWT、httpx、itsdangerous；`itsdangerous` 是 Starlette SessionMiddleware 簽署 session 所需。                                                                                                                             |
| [.env.example](.env.example)                             | 設定名稱範本。正式 secret 只放在未提交的 `.env` 或部署平台 secret store，不要把真實憑證寫進此範例或文件。                                                                                                                                                             |




## 登入流程

```text
Browser
	-> GET /api/auth/google/login
	-> Authlib 建立 OAuth state，導向 Google
	-> Google 驗證使用者，導回 GOOGLE_REDIRECT_URI
	-> 後端檢查 state、交換 authorization code、驗證 OIDC userinfo
	-> 確認 sub、email、email_verified=true
	-> upsert public.member
	-> 簽發 JWT，寫入 HttpOnly cookie
	-> 303 redirect 到 AUTH_SUCCESS_REDIRECT_URL
	-> 前端 GET /api/auth/me（same-origin cookie）
	-> JWT 驗證後，以 member id 查 DB，再回傳 name/email/picture
```



### Google OAuth / OIDC

前端只導向 login endpoint，不直接處理 Google client secret。Authlib 使用 Google 的 OpenID Connect discovery 文件取得授權與 token endpoint。`state` 用來關聯發起與返回的 OAuth 流程並降低 CSRF 風險；FastAPI 的 `SessionMiddleware` 透過 `SESSION_SECRET_KEY` 簽署 session cookie。callback 必須由 login 流程導入，直接在網址列打開 callback 沒有有效 state/code，不能當作登入測試。

後端不以 email 當 Google 唯一識別，而使用 OIDC 的 `sub`（Google account subject）作為 `google_sub` unique key。email 必須存在且 `email_verified` 為 true 才接受。姓名、圖片可能不存在，所以 schema 欄位允許 NULL。

### JWT 與後續 API

JWT claims 包含：


| Claim | 用途                                               |
| ----- | ------------------------------------------------ |
| `sub` | 本系統 `member.id`，不是 email 或 Google subject。       |
| `iss` | 固定 issuer `wke-api`，防止接受其他 issuer 的 token。       |
| `iat` | 簽發時間。                                            |
| `exp` | 到期時間，預設由 `ACCESS_TOKEN_EXPIRE_SECONDS=28800` 控制。 |


演算法固定為 HS256，不接受 token 自行指定其他演算法。瀏覽器使用 `HttpOnly` cookie，JavaScript 無法直接讀取；同時可讓 API client 以 `Authorization: Bearer <JWT>` 傳送。每個受保護 request 除了驗簽與期限，也會以 `sub` 查詢 DB，因此刪除/停用帳號後，舊 token 不會只靠簽章繼續被接受。

生產環境設定 `AUTH_COOKIE_SECURE=true`，只透過 HTTPS 傳送 cookie；`SameSite=Lax` 適用一般 top-level Google redirect callback。`SESSION_SECRET_KEY` 和 `JWT_SECRET_KEY` 必須是彼此不同、不可預測的長隨機值。程式中的 development fallback 不可用於正式部署。

## 資料表與權限

`member` 的重要欄位：


| 欄位                         | 說明                                        |
| -------------------------- | ----------------------------------------- |
| `id`                       | 本系統 identity primary key，JWT 的 `sub`。     |
| `google_sub`               | Google OIDC 穩定識別值，unique；用於 login upsert。 |
| `email`                    | Google 回傳且已驗證的 email。                     |
| `name`, `picture`          | 前端 profile 欄位，可為 NULL。                    |
| `email_verified`           | 只有 Google 回報已驗證時才可登入。                     |
| `created_at`, `updated_at` | 建立與 profile 更新時間。                         |


Repository 使用 `INSERT ... ON CONFLICT (google_sub) DO UPDATE`，所以首次登入新增會員，後續登入更新 Google profile，不會因同一帳號重複建立資料。資料庫 role 至少需要 member 的 SELECT/INSERT/UPDATE，以及 identity sequence 的 USAGE/SELECT。最新 SQL 內的授權概念如下：

```sql
GRANT SELECT, INSERT, UPDATE ON TABLE public.member TO dev_user;
GRANT USAGE, SELECT ON SEQUENCE public.member_id_seq TO dev_user;
```

這些 GRANT 必須由 table/sequence owner 或有授權權限的管理角色執行。修改 SQL 檔本身不會改變已存在資料庫的權限。若正式環境的 API role 不是 `dev_user`，應把 `TO` 後面的角色換成實際 `DATABASE_URL` 使用者。

## 部署設定

正式環境的 OAuth callback URI 必須在 Google Cloud Console 的 OAuth 2.0 Web application client 中登記，且下列值要完全一致：

```text
Google Console Authorized redirect URI
GOOGLE_REDIRECT_URI
https://demo.wke.csie.ncnu.edu.tw/s115999999/api/auth/google/callback
```

scheme、host、deployment prefix、path 及結尾斜線都是比對的一部分。`/callback`、`/google/callback`、是否有尾端 `/` 是不同 URI。使用者瀏覽器在 `/s115999999/` 下方，但反向代理會移除部署前綴後轉送到 Uvicorn；`root_path` 負責告知 FastAPI 外部部署前綴。Google 仍要登記外部瀏覽器可到達的完整 HTTPS URI。

認證相關環境變數：


| 變數                            | 用途                                             |
| ----------------------------- | ---------------------------------------------- |
| `GOOGLE_CLIENT_ID`            | Google OAuth Web client ID。                    |
| `GOOGLE_CLIENT_SECRET`        | Google OAuth client secret；僅後端使用。              |
| `GOOGLE_REDIRECT_URI`         | 完全匹配 Google Console 設定的 callback URL。          |
| `JWT_SECRET_KEY`              | HS256 access token 簽章密鑰。                       |
| `SESSION_SECRET_KEY`          | OAuth state session cookie 簽章密鑰，需與 JWT key 不同。 |
| `AUTH_COOKIE_SECURE`          | HTTPS 部署設為 `true`；僅本機 HTTP 開發才設 `false`。       |
| `ACCESS_TOKEN_EXPIRE_SECONDS` | JWT 有效秒數。                                      |
| `AUTH_SUCCESS_REDIRECT_URL`   | callback 登入完成後的前端 URL，需含 `/s115999999/`。       |


```env.example
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:7777/api/auth/google/callback
JWT_SECRET_KEY=replace-with-a-long-random-secret
SESSION_SECRET_KEY=replace-with-a-different-long-random-secret
AUTH_COOKIE_SECURE=true
ACCESS_TOKEN_EXPIRE_SECONDS=28800
AUTH_SUCCESS_REDIRECT_URL=http://localhost:7777/
```

改動 `.env` 後需重啟 Uvicorn，因為 OAuth client 在模組載入時讀取設定。若 callback 已經失敗，請重新從 login endpoint 發起一次流程，讓新的 state/code 配對完整。

```prompt
Add /api/auth/logout so that user can logout safely.
```



## 本次 Debug 時序



### 1. 找出前端契約

FastAPI workspace 自己的 `public/index.html` 是簡單占位頁；實際網站設定在外部 `C:\code\web\webui`。檢查實際前端後確認：登入連結指向 `/api/auth/google/login`，profile loader 使用 same-origin `GET /api/auth/me`，遇到 401 就維持登入按鈕。故後端採瀏覽器 redirect + cookie，而不是要求前端傳 Google ID token JSON。

### 2. Callback 路徑回 404

曾直接測試 `/s115999999/api/auth/callback/`，回應 `{"detail":"Not Found"}`。當時只有 `/api/auth/google/callback`，路徑確實不一致；後端增加 `/api/auth/callback` 和 `/api/auth/callback/` alias。Google Console 後來確認登記的是 `/api/auth/google/callback`，因此正式 `GOOGLE_REDIRECT_URI` 應採 canonical `/google/callback`，不要為了 alias 把 Console callback 改成另一條路徑。

### 3. Google 回報 request invalid

檢查 `.env` 發現 callback 值末尾有 `/`，但 Google Console 的 Authorized redirect URI 沒有 `/`。OAuth redirect URI 必須完全相同；已將 `.env` 改為無尾斜線的 canonical URL。透過 TestClient 呼叫 login endpoint，從回應 Location 的 query string 取出 `redirect_uri`，實際比對結果與 Console URL 相同。這證明後端送出的值正確，但仍需在部署伺服器重啟後從 login endpoint 重跑整個 OAuth 流程。

### 4. callback 直接開啟與匿名 `/me`

callback URL 直接在瀏覽器開啟時沒有 Google 返回的有效 state/code，不代表 OAuth 流程失敗；callback 應由 `/google/login` 開始。另一個測試發現未登入 `/me` 在 DB dependency 先連線且 DB 不可用時可能回 500。將 security dependency 拆成「先驗 JWT、再查 DB」兩段後，匿名請求可先回 401，不需開 DB connection。已用 TestClient 驗證無 DB 時仍為 401。

### 5. OAuth callback 回 500：確認資料庫權限

使用當時 `.env` 的資料庫設定做唯讀檢查，結果如下：

- PostgreSQL connection 成功，`member` 與 `notes` relation 都存在。
- 從 PostgreSQL catalog 讀到的 `member` 欄位與程式預期相符，identity sequence 為 `public.member_id_seq`。
- 目前連線 role 為 `dev_user`，但 `has_table_privilege` 對 member 的 INSERT 和 SELECT 都是 false；`information_schema.columns` 也因權限不足回傳空集合。

因此 callback 在 `upsert_google_member()` 執行 INSERT/ON CONFLICT 時會因 DB 權限不足失敗，這是當時 500 的已驗證根因。最新 `createtables.sql` 加入 member 與 identity sequence GRANT；但**尚未由工具驗證這些 GRANT 已在實際 DB 執行成功**。需用 owner/admin 執行授權，再重新開始 Google login 流程。

### 6. 測試與驗證記錄

- Pylance 對 auth/security/repository/main 等修改檔案沒有診斷。
- `pip check` 無 broken requirements。
- FastAPI smoke test 確認 health 是公開端點，未設定 OAuth 時 login 回 503，匿名 `/me` 與受保護的 notes 回 401。
- 合成 JWT 測試確認 cookie 與 Bearer 都可驗證；錯誤 JWT 回 401。
- OpenAPI 包含 login 與 `/me`，OAuth callback 隱藏於 schema。
- login response 的 `redirect_uri` 曾經實際抽取並確認為 Google Console 設定的精確 URL。
- 曾出現 Starlette 對 `httpx` TestClient 的 deprecation warning；測試仍成功，這不是 callback 500 的原因。
- 真正的 Google-to-Google code exchange 與成功後 member upsert 尚未在本機端到端重跑；需先套用資料庫 GRANT，並在部署環境從 login endpoint 完整測試。



## 安全與維運提醒

- 本次對話曾貼出 Google client secret；應立即在 Google Cloud Console 輪替該 secret，更新部署環境後再撤銷舊值。此文件不保存該值。
- `AUTH_COOKIE_SECURE=true`，確保只有在https時傳送。
- 若 `JWT_SECRET_KEY` 或 `SESSION_SECRET_KEY` 仍是範例 placeholder，請先換成兩個互不相同的高熵隨機值。更換 JWT key 會使既有 JWT 全數失效；更換 session key 會使進行中的 OAuth state session 失效，需要重新登入。
- 不要把 `.env`、OAuth secrets、JWT、cookie 值或帶 authorization code 的完整 callback URL commit 到 Git、issue 或文件。
- 執行 `psql/createtables.sql` 前先修復目前檔尾未完成的 `SELECT *`。此腳本前段會 `DROP TABLE IF EXISTS notes`，正式 DB 請採非破壞性的 migration 或只執行需要的 member/GRANT SQL。



### 足弓小幫手：OAuth 2.0、OpenID Connect、JWT 各自做什麼

Google 負責證明「這個人是誰」，自己的後端負責發一張通行證。之後瀏覽器拿這張通行證問 `/api/auth/me`。

**OAuth 2.0** 是授權流程。使用者在 Google 登入並同意網站讀取基本資料後，Google 把瀏覽器帶回 callback，並附上一次性的 `code`。後端用這個 `code` 向 Google 換資料。使用者的 Google 密碼不會進這支程式。

**OpenID Connect** 是加在 OAuth 2.0 上面的身份層。程式向 Google 要的範圍是 `openid email profile`。換回來的 `userinfo` 才有「這個人是誰」：`sub`（Google 帳號的固定編號）、`email`、`name`、`picture`、`email_verified`。`member` 以 `google_sub` 當唯一鍵。

**JWT** 是後端自己簽的通行證，不是 Google 那張。`create_access_token` 用 `JWT_SECRET_KEY` 做 HS256 簽名，內容只有四個欄位：`sub`（自己的 `member.id`）、`iss`（`foot-helper`）、`iat`（簽發時間）、`exp`（到期時間）。之後 `/api/auth/me`、`notes`、`subclass` 認的是這張，不再問 Google。

### JWT 放在 localStorage、sessionStorage、HttpOnly cookie 的風險

目前放的是 **HttpOnly cookie**，名稱 `access_token`。`httponly=True`，網頁上的 JavaScript 讀不到；學校站 `secure` 為 true，只走 HTTPS；`samesite=lax`，別的網站用表單或腳本打這個 API 時，瀏覽器通常不會帶上這張 cookie。`max_age` 預設 8 小時（`ACCESS_TOKEN_EXPIRE_SECONDS=28800`）。


| 存放位置             | 網頁上的 JavaScript 能不能讀到 | 關掉分頁後還在不在           | 主要風險                                         |
| ---------------- | --------------------- | ------------------- | -------------------------------------------- |
| `localStorage`   | 能                     | 還在，直到被清掉            | 網站若被植入惡意腳本（XSS），腳本可以直接把 JWT 複製走，之後在別處重放      |
| `sessionStorage` | 能                     | 關掉該分頁就沒了            | 同樣可被 XSS 讀走，竊取窗口限在這個分頁還開著的時候                 |
| HttpOnly cookie  | 不能                    | 依 `max_age`，預設 8 小時 | 腳本複製不走字串；若網站自己被 XSS，腳本仍可請瀏覽器帶著 cookie 去打 API |


HttpOnly 擋的是「把通行證原文偷走」。它擋不住「惡意腳本就在這個網站裡、請瀏覽器代送 cookie」。

### JWT 被改過、過期、帳號刪了、cookie 被清掉

四種最後都是 **401**。前端 `auth.js` 收到失敗就回到「登入」。差在後端哪一步擋下來。


| 情況                                          | 後端怎麼判斷                                          | 回應                      |
| ------------------------------------------- | ----------------------------------------------- | ----------------------- |
| JWT 被改過                                     | 簽名對不上 `JWT_SECRET_KEY`，或 `iss` 不是 `foot-helper` | 401，`Invalid token`     |
| JWT 過期                                      | `exp` 已過（預設簽發後 8 小時）                            | 401，`Invalid token`     |
| 帳號從 `member` 刪了，或 `email_verified` 不再是 true | 簽名仍有效，但 `get_verified_member` 查不到               | 401，`User not found`    |
| cookie 被清掉                                  | 請求裡沒有 `access_token`                            | 401，`Not authenticated` |


前兩種在驗簽時就結束，不會去查資料庫。帳號被刪是簽章通過之後才查庫。cookie 被清掉則連字串都沒有。

### 從按登入到 `/api/auth/me`

```mermaid
sequenceDiagram
    participant 瀏覽器
    participant 你的後端
    participant Google
    participant PostgreSQL

    瀏覽器->>你的後端: 開啟頁面，auth.js 呼叫 GET /api/auth/me
    你的後端-->>瀏覽器: 401，右上角顯示「登入」
    瀏覽器->>你的後端: 點「登入」，GET /api/auth/google/login
    你的後端-->>瀏覽器: 導向 Google 登入頁
    瀏覽器->>Google: 使用者登入並同意
    Google-->>瀏覽器: 導回 /api/auth/google/callback?code=...
    瀏覽器->>你的後端: 帶著 code 打開 callback
    你的後端->>Google: 用 code 換 userinfo
    Google-->>你的後端: sub、email、name、picture
    你的後端->>PostgreSQL: 依 google_sub 新增或更新 member
    PostgreSQL-->>你的後端: member.id
    你的後端-->>瀏覽器: 303 回到首頁，Set-Cookie access_token
    瀏覽器->>你的後端: 頁面再載入，GET /api/auth/me（瀏覽器自動帶 cookie）
    你的後端->>你的後端: 驗簽名、iss、exp，取出 sub
    你的後端->>PostgreSQL: 用 member.id 查已驗證會員
    你的後端-->>瀏覽器: 200，name、email、picture
```



對到檔案，順序是：

1. 每個頁面載入 `js/auth.js`，先打 `GET api/auth/me`。沒有 cookie 就 401，右上角維持「登入」，連結指向 `api/auth/google/login`。
2. 點下去後，`google_login` 把瀏覽器送到 Google。
3. Google 把人送回 `GOOGLE_REDIRECT_URI`，也就是 `/s115321503/api/auth/google/callback`。
4. `google_callback` 用 `code` 換 `userinfo`。沒有 `sub`、沒有 email、或 email 未驗證，就 401。
5. `upsert_google_member` 以 `google_sub` 寫入 `member`。同一人再登入會更新名稱和頭貼，不會多一筆。
6. `create_access_token(member.id)` 簽自己的 JWT，放進 HttpOnly cookie，然後 303 回首頁。
7. 首頁再跑一次 `auth.js`。這次 cookie 會自動附上。`get_current_member` 先验 JWT，再依 `sub` 查 `member`，回傳名稱、email、頭貼網址。`showSignedIn` 顯示名字＋頭像；點頭像可開「個人設定／登出」。

---



### 本週筆記：登入綁 API＋側欄接 `vd_subclass`

W05 的目錄 view 與 W06 的 JWT 在專案裡接在一起。分層說明見 `[architecture.md](architecture.md)`。

**後端（本 repo）**


| 層            | 檔案                                       | 做什麼                                                   |
| ------------ | ---------------------------------------- | ----------------------------------------------------- |
| 保護路由         | `routers/subclass.py`、`routers/notes.py` | `dependencies=[Depends(get_current_member)]`，沒票 → 401 |
| 驗票           | `core/security.py`                       | 讀 cookie／Bearer、驗 JWT、再查 `member`                     |
| SQL          | `repositories/subclass.py`               | `SELECT ... FROM vd_subclass WHERE pcid = %s`         |
| 登入／me／logout | `routers/auth.py`                        | Google OIDC → upsert → 設／清 `access_token`             |
| 無副檔名靜態頁      | `main.py` 的 `HtmlCssOnlyStaticFiles`     | `/scan` → `webui-lab/scan.html`                       |


**前端（**`webui-lab`**，筆記在** `docs/web.md` **W06）**


| 檔案           | 做什麼                                               |
| ------------ | ------------------------------------------------- |
| `js/auth.js` | `GET api/auth/me`；登出 `POST api/auth/logout`       |
| `js/nav.js`  | `GET api/subclass/pcid/1`；401 不畫掃描／運動／菜單，並擋直接開那些頁 |
| 各頁底部導覽       | 總覽、教學寫死；中間 `#nav-subclass` 由 API 填                |


**資料（本機** `fastapi_dev`**）**

```sql
-- 側欄用的三列（hahahan 的子節點）
SELECT pcid, parent_name, cid, child_name
FROM vd_subclass
WHERE pcid = 1
ORDER BY cid;
-- → 掃描、運動菜單、運動
```

教學頁不進 `class`。表擁有者是 `hahahan`；用 `dev_user` 直接 `SELECT` 會 permission denied，那是 DB GRANT，和 API 的 401 不同層。

**為什麼權限鎖在 API**

靜態 HTML 誰都能開。真正不能匿名拿的是 JSON。前端藏連結只是 UX；沒有有效 JWT，`/api/subclass/pcid/1` 進不了 repository。

### 驗收對照（W06 專案）

- [x] Google 登入後有 `member` 列；`/api/auth/me` 回 profile
- [x] 未登入：`/api/auth/me`、`/api/subclass/pcid/1`、`/api/notes` → 401
- [x] 登入後側欄出現掃描／運動菜單／運動；登出後消失
- [x] 分層：router 不寫 SQL；SQL 在 repository；登入檢查在 `get_current_member`
- [ ] （選）`dev_user` 只 `GRANT SELECT` 給需要的 view／表（最小授權）

---

---

## W07 :EER Model and AI Gen Data {#EER}
EER設計與AI產生測資

### AI Chat問清楚設計
開始前先準備好大量測試資料，AI coding可以幫大忙：
> # Postgresql
> 根據EER設計，大部分entity tables可以繼承object, e.g. member, course, section。根據大學現況，faculty, staff, student can inherit from member. 請修改academic.sql依此設計簡易教務系統DB，給我academic_EER.sql

```EER of Object
Object (oid)
│
├── Member (oid PK/FK)
│   ├── Faculty (oid PK/FK)
│   ├── Staff   (oid PK/FK)
│   └── Student (oid PK/FK)
│
├── Department (oid PK/FK)
├── Semester   (oid PK/FK)
├── Course     (oid PK/FK)
└── Section    (oid PK/FK)
```

```sql
CREATE SCHEMA IF NOT EXISTS academic_eer;   -- Isolated schema for EER tables, views, and functions.
SET search_path TO academic_eer, public;    -- Use academic_eer first, then public schema.

-- ===== 1. Original generic class/object model (preserved) =====
CREATE TABLE IF NOT EXISTS class (...)
...

CREATE OR REPLACE VIEW vd_section_roster AS
SELECT sec.oid AS section_oid, co.course_code, co.course_name,
       sem.academic_year, sem.term, sec.section_no,
       st.student_no, m.full_name AS student_name,
       e.status AS enrollment_status, e.final_grade
FROM ss e
JOIN section sec ON sec.oid=e.section_oid
JOIN course co ON co.oid=sec.course_oid
JOIN semester sem ON sem.oid=sec.semester_oid
JOIN student st ON st.oid=e.student_oid
JOIN member m ON m.oid=st.oid;

COMMIT;
```

```shell
psql -U postgres -d postgres -v DBName=fastapi_dev -f academic_EER.sql
```

- 建立 `schema` `academic_eer` 方便資安於獨立使用。Data model設計清楚後，就可以善用AI。
- 思考慣用JOIN寫法 vs. 老師上課教的寫法。

### VSCode + Codex
為了解省Github Copilot free tokens，大量測資以codex產生：
- Extension > search Codex > 安裝好一陣子 (C:\Users\xxx\.vscode\extensions\openai.chatgpt-26.51007.21434-win32-x64, 1.7GB)
- 完成：Chat旁邊Tab多了 `Codex`，在此聊天。 /status /plan
- 要求Browser Session of ChatGPT (先瀏覽器登入)

> set current working directory to ./psql/acdeamic

> /plan check and verify academic_EER.sql and summarize docs into ./psql/readme.md

Plan:
1. Review psql/academic_EER.sql against the other SQL scripts and application queries.
2. Verify it in an isolated PostgreSQL database: initial execution, repeat execution, seed hierarchy, foreign keys, overlapping member roles, classification triggers, and views.
3. Record defects and distinguish enforced constraints from application responsibilities.
4. Create ./psql/readme.md summarizing script purposes, setup commands, EER relationships, verification results, and API integration requirements.
...
PostgreSQL 18 tools are available locally. No files have been changed.

> Keep my revises (e.g. ss replace enrollment) in academic_EER.sql and do it.

Done. Preserved your revisions, including sf, ss, sta, and md.
...
- 自動產生 `verify_academic_EER.sql` 有興趣自己學習

> create vdata.sql to generate virtual data (unicode traditional chinese) for simulating ncnu.edu.tw.
> 1. 5 departments, must contain CSIE
> 2. 111-1 to 115-1 semester (2 semesters per year start from Feb 1 and Sep 1 respectively)
> 3. Each department has 90 ~ 150 courses with 20 ~ 30 course sections for each semester
> 4. Each department has 30 students for each admission_year, student_no is s115ddnnnn, dd is department no and nnnn is serial no.
> . Each department has 10 faculties and 2 staffs.
> 6. Each faculty offer (sf relationship) 2 ~ 5 course sections for each semester. Naming e.g. 周杰倫、蔡依林 for example. Don't use real name from ncnu. Students use the same naming policy.
> 7. Each student enrolls (ss relationship) 4 ~ 9 sections for each semester.
8. You can add other virtual data that I did not consider.

Verified fresh and repeat runs on PostgreSQL 18: 5 departments, 600 courses, 1,133 sections, 750 students, 50 faculty, and 10 staff. Teaching and enrollment ranges pass.
```powershell
psql -X -U postgres -d academic_eer_demo -f .\psql\academic\vdata.sql
```
因為codex沒有先前copilot聊天記憶，db應修改：
```powershell
psql -X -U postgres -d fastapi_dev -f .\psql\academic\vdata.sql
```

> psql:psql/academic_EER.sql:74: ERROR:  character with byte sequence 0x96 0xe9 in encoding "BIG5" has no equivalent in encoding "UTF8"

psql is interpreting your UTF-8 SQL file as BIG5, causing the Chinese text conversion to fail.
I verified the file is valid UTF-8 and added this immediately after \connect in [academic_EER.sql (line 20)](/C:/code/psql/api/psql/academic_EER.sql:20):
```sql
\encoding UTF8
```

> Add test.sql so that I can run selected sql statements within the file in VScode to check data rows.

> 我不習慣JOIN寫法，習慣用FROM列出所已有table alias, ...，WHERE 寫T1.PK = T2.FK1 and T2.FK2 = T3.PK的寫法，這樣對應ER/EER model思考比較清楚。參考view vd_subclass的寫法，將test.sql用到JOIN的statements都改寫，並add to new test_wke.sql

```sql JOIN
SELECT p.cid as pcid, p.name as parent_name, c.cid as cid, c.name as child_name
FROM inheritance i
INNER JOIN class p
    ON p.cid = i.pcid
INNER JOIN class c
    ON c.cid = i.ccid;
```

```sql wke-style
SELECT p.cid as pcid, p.name as parent_name, c.cid as cid, c.name as child_name
FROM class p, inheritance i, class c
WHERE p.cid = i.pcid AND c.cid = i.ccid;
```

逐步檢視資料，發現問題：所有學號都是s115ddnnnn

> update student_no by rule: s<adminion_year>ddnnnn. E.g. if adminion_year = 111 then set 's115010121' to 's111010121'。SQL寫於vdata.sql最後

```sql
-- 依入學年度更新學號，保留 ddnnnn；可在 VS Code 單獨選取執行。
-- 例：admission_year=111，s115010121 -> s111010121。
UPDATE academic_eer.student st
SET student_no = 's' || st.admission_year::text || right(st.student_no, 6)
--select 's' || st.admission_year::text || right(st.student_no, 6)
--from academic_eer.student st
WHERE st.admission_year IS NOT NULL
  AND st.student_no ~ '^s[0-9]+[0-9]{6}$'
--  AND st.student_no IS DISTINCT FROM
--      's' || st.admission_year::text || right(st.student_no, 6);
```

>add academic_views.sql: create views from schema.academic_eer and can be accessed by schema.public with dev_user account.
> 1. eer_subclass: according to vd_subclass and extending columns(pcid, pname, cid, name, des, namepath, idpath, des)

```sql
-- Same direct parent/child relationship as academic_eer.vd_subclass.
-- des, namepath and idpath describe the child class.
-- The requested duplicate des column is included once (view columns must be unique).
-- Default view-owner permissions allow dev_user to query this view without
-- granting direct access to the academic_eer tables.
CREATE OR REPLACE VIEW public.eer_subclass AS
SELECT p.cid AS pcid,
       p.name AS pname,
       c.cid AS cid,
       c.name AS name,
       c.des AS des,
       c.namepath AS namepath,
       c.idpath AS idpath
FROM academic_eer.class p,
     academic_eer.inheritance i,
     academic_eer.class c
WHERE p.cid=i.pcid
  AND i.ccid=c.cid;

GRANT USAGE ON SCHEMA public TO dev_user;
GRANT SELECT ON TABLE public.eer_subclass TO dev_user;
```

### Github Copilot
建立 `public.eer_subclass` 從 `academic_eer` schema取得資料：API需修改，也會連帶稍微改到Web。
> 登入OAuth後，由db取得member.id，作為 subclass/pcid/{id} 參數

目前 OAuth callback 已把資料寫入 member，但登入後的 /auth/me 沒有回傳 id；前端載入 subclass 時則把 pcid 寫死為 4。我會讓已驗證的會員資料提供資料庫 id，並確認首頁的載入流程可用它呼叫 API。

我會調整 /auth/me 回傳資料包含資料庫 member.id，再讓首頁先取登入者資料，以該 id 載入 subclass/pcid/{id}；未登入時仍顯示既有登入提示，主控台卡片照常載入。

已完成 OAuth 後以資料庫會員 ID 載入 subclass：
- auth.py：/auth/me 現在會回傳資料庫的 member.id。
- app.js：首頁先取得登入資料，再用其中的 ID 呼叫 /subclass/pcid/{id}；未登入時維持原有提示，主控台卡片仍會載入。
- 同步更新 README.md 與 oauth.md 的 API 說明。

#### Web
前端程式中，member.id 不是從 OAuth token 直接取出，而是由後端的登入資料 API 回傳。實際使用的欄位名稱是 profile.id。流程如下：
- index.html 的登入連結會導向 api/auth/google/login，開始 Google OAuth。
- Google 驗證完成後，後端應驗證 Google 身分，並建立自己的登入 session。通常後端會用 Google 身分找到或建立系統內的會員，取得該會員的 member.id。
- 前端呼叫 GET api/auth/me，並透過同源 session cookie 帶上登入狀態。回應會被解析成 profile：loadAccountProfile。
- loadPageData 讀取 profile.id，檢查它是正整數後，呼叫 api/subclass/pcid/{profile.id}。

因此，後端的 auth/me 回應需要包含內部會員 ID (自建立之DB)，例如：
```json
{
  "id": 1,
  "name": "XXX",
  "email": "XXX@gmail.com",
  "picture": "https://lh3.googleusercontent.com/a/ACg8ocI-GK9-7nOeHTh0dSbQnD9nUhI8be6LthNw6yMEsDY_r0f0RFk=s96-c"
}
```

要注意，Google 的使用者識別值（例如 Google ID／sub）不一定等於你們系統的 member.id。若 API 回應沒有 id，前端會顯示「登入資料缺少有效會員識別碼」，也無法用這個 ID 載入選單。

---

## W08：Schema and Reuse Data Views{#ReuseView}

利用Schema於data model隔離，並善用eer_subclass讓API可以reuse

### PostgreSQL Schema：概念與運用

#### 1. Schema是什麼？

在PostgreSQL中，**Schema是Database內部用來組織與管理資料庫物件的命名空間（Namespace）**。

一個Database可以包含多個Schema，而每個Schema可以包含Tables、Views、Functions、Sequences等物件。

```text
PostgreSQL Server
│
├── Database: fastapi_dev
│   │
│   ├── Schema: public (預設)
│   │   ├── member
│   │   └── course
│   │
│   └── Schema: academic_eer
│       ├── object
│       ├── member
│       ├── faculty
│       ├── student
│       ├── course
│       ├── section
│       └── enrollment
│
└── Database: other_db
    └── Schema: public
```

**重點：**
- Database是資料庫的主要隔離單位。
- Schema是同一Database內的邏輯分組與命名空間。
- 不同Schema可以存在同名Table，例如`public.member`與`academic_eer.member`。
- Schema不等於獨立Database，Schema之間可以透過SQL JOIN與Foreign Key建立關聯。
- Schema也可作為權限管理的邊界，但不代表資料自動隔離。

#### 2. 為什麼使用Schema？

| 用途 | 說明 |
|---|---|
| 模組化 | 將教務、財務、人事資料表分組 |
| 避免命名衝突 | 不同Schema可以有同名Table |
| 權限管理 | 控制使用者能存取哪些Schema及物件 |
| 版本並存 | 例如`academic_v1`、`academic_v2` |
| 開發測試 | 將測試用物件與正式物件分開 |

例如，大學系統可規劃：

```text
university_db
├── academic    # 教務
├── hr          # 人事
├── finance     # 財務
└── public      # 共用或預設物件
```

#### 3. Schema基本SQL操作

**建立Schema**

```sql
CREATE SCHEMA academic_eer;
```

**建立Table到指定Schema**

```sql
CREATE TABLE academic_eer.member (
    oid BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

**查詢指定Schema的Table**

```sql
SELECT * FROM academic_eer.member;
```

**SQL：列出Schema and Tables**

```sql
SELECT schema_name FROM information_schema.schemata
WHERE schema_name NOT IN ('information_schema') AND schema_name NOT LIKE 'pg_%';

SELECT table_name FROM information_schema.tables
WHERE table_schema = 'academic_eer' AND table_type = 'BASE TABLE';
```

**刪除Schema**

```sql
DROP SCHEMA academic_eer;
```

若Schema內還有Table等物件，通常無法直接刪除。

```sql
DROP SCHEMA academic_eer CASCADE;
```

注意：`CASCADE`會連同內部物件及相依物件一併刪除，可能造成資料遺失。

#### 4. search_path：決定SQL預設使用哪個Schema

如果執行：

```sql
SELECT * FROM member;
```

PostgreSQL如何知道要查詢哪個Schema的`member`？

答案是透過`search_path`。

**查看目前設定**

```sql
SHOW search_path;
```

常見預設值：

```text
"$user", public
```

代表先尋找與目前使用者同名的Schema，再尋找`public`。

**設定目前Session的Schema搜尋順序**

```sql
SET search_path TO academic_eer, public;
```

之後：

```sql
SELECT * FROM member;
```

會優先查詢`academic_eer.member`。

也可以明確指定：

```sql
SELECT * FROM public.member;
SELECT * FROM academic_eer.member;
```

- **注意：**`SET search_path`通常只影響目前的資料庫連線（Session），不會永久修改所有連線設定。
- 若要設定預設順序於整個DB：

```sql
ALTER DATABASE fastapi_dev SET search_path TO academic_eer, public;
```

#### 5. Schema與EER的差異

這兩個名詞容易混淆：

| 名詞 | 意義 |
|---|---|
| Database Schema | 資料庫的邏輯結構定義，也可泛指Tables、Constraints等設計 |
| PostgreSQL Schema | Database內的Namespace |
| EER（Enhanced ER Model） | 描述Entity、Relationship、Inheritance等概念的資料模型 |

例如：

```text
academic_eer (PostgreSQL Schema)
│
├── object
├── member
├── faculty
├── staff
└── student
```

其中`academic_eer`只是Namespace。

而以下是EER的概念繼承：

```text
Object
  └── Member
       ├── Faculty
       ├── Staff
       └── Student
```

**Schema本身不會實現EER繼承。** 繼承關係需要透過資料表設計，例如Shared Primary Key（PK同時為FK）實作。

#### 6. Schema權限管理

例如建立一個只能查詢教務資料的使用者：

```sql
CREATE ROLE academic_reader LOGIN PASSWORD 'change_me';

GRANT CONNECT ON DATABASE fastapi_dev TO academic_reader;

GRANT USAGE ON SCHEMA academic_eer TO academic_reader;

GRANT SELECT ON ALL TABLES IN SCHEMA academic_eer
TO academic_reader;
```

- `CONNECT`：允許連線至Database。
- `USAGE`：允許解析Schema內的物件名稱。
- `SELECT`：允許讀取授權的Tables。

`USAGE`本身不代表可以讀取Table資料。

上述`GRANT SELECT ON ALL TABLES`只涵蓋目前已存在的Tables。未來新增的Tables需要另外設定Default Privileges或重新授權。

#### 7. 實務設計建議

以簡易大學教務系統為例：

- **單一系統、資料表數量少：** 可以先使用`public`。
- **多模組系統：** 可以使用`academic`、`hr`、`finance`分組。
- **EER架構實驗：** 使用`academic_eer`，避免與原本`public`中的資料表衝突。
- **正式環境：** 建議明確指定Schema、設定最小權限，避免不可信使用者在應用程式的`search_path`中建立物件。

**核心觀念：**

> Database負責資料庫層級的隔離，Schema負責Database內部的命名與組織，Table負責實際儲存資料，而EER負責描述資料的實體、關聯與繼承結構。

### Reuse `eer_subclass`

- 原設計：無法得知目錄是否內含物件可以click → eer_co to get list objects 
```sql
SELECT p.cid AS pcid,
       p.name AS pname,
       c.cid AS cid,
       c.name AS name,
       c.des AS des,
       c.namepath AS namepath,
       c.idpath AS idpath
FROM academic_eer.class p,
     academic_eer.inheritance i,
     academic_eer.class c
WHERE p.cid=i.pcid AND i.ccid=c.cid;
```

- 加入count(*) > 0代表co存在 → click to show objects
```sql
drop view public.eer_subclass; -- view欄位變化須要刪除重寫
CREATE OR REPLACE VIEW public.eer_subclass AS
SELECT p.cid AS pcid, p.name AS pname, c.cid AS cid, c.name AS name, c.namepath AS namepath, c.idpath AS idpath, count(co.cid) as n
FROM class p, inheritance i, class c
LEFT JOIN co ON c.cid = co.cid  -- LEFT JOIN讓n = 0時，資料還是會出現
WHERE i.ccid = c.cid and i.pcid = p.cid
GROUP BY p.cid, c.cid, c.name, c.namepath, c.idpath;

GRANT USAGE ON SCHEMA public TO dev_user;
GRANT SELECT ON TABLE public.eer_subclass TO dev_user;
```

- 預設首頁資料
```sql
select * from eer_subclass where pcid = 0 order by n;
```
- 個人功能目錄
```sql
select * from eer_subclass where pcid = 0 order by cid;
```

#### eer_co

已知cid取得目錄物件列表。**注意：** schema預設：academic_eer → public
```sql
CREATE OR REPLACE VIEW public.eer_co AS
SELECT c.cid, c.name, o.oid, o.title, o.entity, o.entity_data
FROM class c, co, eer_objectDetail o
WHERE c.cid = co.cid and co.oid = o.oid
order by o.oid;
GRANT SELECT ON TABLE public.eer_co TO dev_user;

select * from eer_co where cid = 31;
```



#### github copilot
> 新增 /api/root 對應 api/subclass/pcid/0。但是盡量reuse現有codes

> /api/root 視為public，不須登入

> add /api/root/co/{cid} to get select * from public.eer_co where cid = {cid}

> #sym:get_subclasses_by_pcid 檢查並調整為最佳寫法
- 僅排序方式不同，加入 `order_by` 參數
```python
def get_subclasses_by_pcid(
    connection: psycopg.Connection,
    pcid: int,
    order_by: Literal["cid", "n"],
) -> list[dict[str, Any]]:
    """Return subclass rows for a parent class ID, ordered by a supported column."""

    query = sql.SQL(
        "SELECT * FROM eer_subclass WHERE pcid = %s ORDER BY {}"
    ).format(sql.Identifier(order_by))
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query, (pcid,))
        return cursor.fetchall()
```
- public API
```python
@api_router.get("/root", tags=["subclass"])
def read_root_subclasses(
    connection: psycopg.Connection = Depends(get_db_connection),
) -> list[dict[str, object]]:
    """回傳根節點（pcid=0）底下的 subclass。"""

    return get_subclasses_by_pcid(connection, 0, "n")
```
- member API： `dependencies=[Depends(get_current_member)]`
```python
router = APIRouter(
    prefix="/subclass",
    tags=["subclass"],
    dependencies=[Depends(get_current_member)],
)

@router.get("/pcid/{id}")
def read_subclasses_by_pcid(
    id: int,
    connection: psycopg.Connection = Depends(get_db_connection),
) -> list[dict[str, object]]:
    """依照 parent class id 回傳所有 subclass。"""

    return get_subclasses_by_pcid(connection, id, "cid")
```



---

## W9：進階查詢：分頁、篩選、搜尋 {#paging}

### 1. 學習目標

實作實務系統必備的資料查詢功能：
- Pagination：分頁，避免一次載入大量資料。
- Filtering：依照條件動態篩選資料。
- Searching：使用關鍵字搜尋資料。
- Sorting：依照指定欄位排序。
- 比較 FastAPI 與 PostgreSQL VIEW 的實作方式。
- 理解 API、Database 的職責分工及資安問題。

**核心問題：查詢邏輯應該放在 FastAPI，還是 PostgreSQL？**

### 2. 系統架構
假設建立一個課程查詢系統，資料庫包含：
```sql
CREATE TABLE courses (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(100) NOT NULL,
  department VARCHAR(50) NOT NULL,
  credits INTEGER NOT NULL CHECK (credits > 0),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

API 提供：
```http
GET /courses?page=1&size=10
GET /courses?department=CS
GET /courses?keyword=Python
GET /courses?department=CS&keyword=Web&page=2&size=10
```

回傳 JSON：
```json
{
  "items": [
    {
      "id": 1,
      "code": "CS101",
      "name": "Web Programming",
      "department": "CS",
      "credits": 3
    }, ...
  ],
  "total": 25,
  "page": 1,
  "size": 10,
  "total_pages": 3
}
```

#### 基本 SQL

**分頁（Pagination）**
```sql
SELECT *
FROM courses
ORDER BY id
LIMIT 10 OFFSET 20;
```
- LIMIT：最多回傳 10 筆。
- OFFSET：跳過前 20 筆。
- 對應第 3 頁，每頁 10 筆。

公式：
```python
offset = (page - 1) * size
```

**篩選（Filtering）**
```sql
SELECT *
FROM courses
WHERE department = 'CS'
  AND is_active = TRUE;
```

**搜尋（Searching）**
```sql
SELECT *
FROM courses
WHERE name ILIKE '%Python%';
```
- LIKE：依資料庫的比較規則進行字串比對。
- ILIKE：PostgreSQL 不區分英文大小寫的比對。
- `%`：萬用字元，可代表任意長度的字串。

注意：`ILIKE '%keyword%'` 在大量資料時可能效率不佳。

### 3. 方法 A：FastAPI 動態組合 SQL

#### 3.1 架構

```text
Frontend (React / JavaScript)
          |
          | GET /courses?department=CS&keyword=Web
          v
FastAPI
  ├── 驗證查詢參數
  ├── 動態組合 WHERE
  ├── 執行 COUNT(*)
  ├── 計算 LIMIT / OFFSET
  └── 回傳 JSON
          |
          v
PostgreSQL courses table
```

#### 3.2 FastAPI 範例
使用 `psycopg` 3，假設已建立資料庫連線設定。
```python
from fastapi import FastAPI, Query
from psycopg.rows import dict_row
import psycopg
import math
import os

app = FastAPI()

DATABASE_URL = os.environ["DATABASE_URL"]

@app.get("/courses")
def get_courses(
  page: int = Query(1, ge=1),
  size: int = Query(10, ge=1, le=100),
  department: str | None = None,
  keyword: str | None = None
):
  conditions = []
  params = []

  if department:
    conditions.append("department = %s")
    params.append(department)

  if keyword:
    conditions.append("name ILIKE %s")
    params.append(f"%{keyword}%")

  where_sql = (
    " WHERE " + " AND ".join(conditions)
    if conditions else ""
  )

  offset = (page - 1) * size

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor(row_factory=dict_row) as cur:
      cur.execute(
        "SELECT COUNT(*) AS total FROM courses" + where_sql,
        params
      )
      total = cur.fetchone()["total"]

      cur.execute(
        "SELECT id, code, name, department, credits "
        "FROM courses" + where_sql +
        " ORDER BY id LIMIT %s OFFSET %s",
        params + [size, offset]
      )
      items = cur.fetchall()

  return {
    "items": items,
    "total": total,
    "page": page,
    "size": size,
    "total_pages": math.ceil(total / size)
  }
```

#### 3.3 特點
優點：
- API 邏輯集中於 Python，容易理解與除錯。
- 可根據不同條件動態建立 WHERE。
- 易於整合 Pydantic、JWT、Authentication。
- 適合 API 專屬的查詢需求。

缺點：
- 多支 API 可能重複撰寫 JOIN、WHERE。
- 複雜 SQL 會讓 Python 程式碼難以維護。
- 查詢邏輯與 API 邏輯可能高度耦合。
- 必須嚴格防範 SQL Injection。

### 4. 方法 B：PostgreSQL VIEW + FastAPI

#### 4.1 VIEW 是什麼？
VIEW（檢視表）是一個**儲存在資料庫中的查詢定義**。

一般 VIEW 不會另外儲存查詢結果，而是在查詢時由 PostgreSQL 執行及最佳化。例如：
```sql
CREATE VIEW v_active_courses AS
SELECT
  id,
  code,
  name,
  department,
  credits
FROM courses
WHERE is_active = TRUE;
```

使用方式：
```sql
SELECT *
FROM v_active_courses
WHERE department = 'CS'
ORDER BY id
LIMIT 10 OFFSET 0;
```

VIEW 可以視為一個可重複使用的資料查詢介面。

#### 4.2 架構

```text
Frontend (React / JavaScript)
          |
          v
FastAPI
  ├── 驗證參數
  ├── 動態篩選
  ├── Pagination
  └── JSON Response
          |
          v
PostgreSQL VIEW
  └── v_active_courses
          |
          v
PostgreSQL TABLE
  └── courses
```

#### 4.3 FastAPI 查詢 VIEW

沿用前面範例的 FastAPI 程式，只需要將：
```python
"FROM courses"
```

修改為：
```python
"FROM v_active_courses"
```

便能使用 VIEW 提供的資料。例如：
```sql
SELECT *
FROM v_active_courses
WHERE department = 'CS'
  AND name ILIKE '%Web%'
ORDER BY id
LIMIT 10 OFFSET 0;
```

**注意：VIEW 不會自動實作分頁、動態篩選或搜尋。**

VIEW 負責提供一致的資料集合；FastAPI 仍負責接收參數、執行查詢與回傳結果。

### 5. VIEW 的進階應用：封裝 JOIN

VIEW 真正有價值的地方，是將多個資料表的複雜查詢封裝起來。

假設另有系所資料表：
```sql
CREATE TABLE departments (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  code VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL
);
```

建立跨資料表 VIEW：
```sql
CREATE VIEW v_course_details AS
SELECT
  c.id,
  c.code,
  c.name,
  c.credits,
  d.name AS department_name
FROM courses c
JOIN departments d
  ON c.department = d.code
WHERE c.is_active = TRUE;
```

FastAPI 不需要知道 JOIN 細節：
```sql
SELECT *
FROM v_course_details
WHERE department_name ILIKE '%資訊%'
ORDER BY id
LIMIT 10 OFFSET 0;
```

優點：
1. 多支 API 可共用同一個 VIEW。
2. 避免重複撰寫複雜 JOIN。
3. 資料表結構與 API 查詢介面適度解耦。
4. 修改內部 JOIN 時，可降低對 API 的影響。

但 VIEW 欄位變更仍可能破壞既有 API，因此需要管理資料庫 Schema Migration。

### 6. FastAPI vs. PostgreSQL VIEW 比較

| 比較面向 | FastAPI 直接查詢 | PostgreSQL VIEW + FastAPI |
|---|---|---|
| SQL 邏輯 | Python 程式內 | 部分封裝於 VIEW |
| 動態篩選 | 容易 | 仍由 API 傳入條件 |
| 關鍵字搜尋 | SQL WHERE | SQL WHERE |
| Pagination | LIMIT / OFFSET | LIMIT / OFFSET |
| 複雜 JOIN | 需在 API 撰寫 | 可封裝於 VIEW |
| 程式碼重複 | 可能較多 | 可減少 |
| 維護方式 | 修改 Python | 修改 VIEW 或 Python |
| 權限控制 | API + DB | API + DB，可配合 VIEW 權限 |
| 查詢效能 | 依 SQL 與索引 | 通常與等價 SQL 接近 |
| 適用情境 | 簡單、動態查詢 | 複雜、重複使用的資料查詢 |

#### 效能的重要觀念

**一般 VIEW 不等於快取，也不保證查詢更快。**

PostgreSQL 通常會將 VIEW 展開並進行查詢最佳化。因此：
```sql
SELECT * FROM v_active_courses;
```

與等價的原始 SQL，通常具有接近的執行計畫。真正影響效能的因素包括：
- Index 是否適當。
- WHERE 是否能有效利用索引。
- JOIN 的成本。
- 資料筆數與分布。
- OFFSET 大小。
- 查詢執行計畫。

可使用：
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM v_active_courses
WHERE department = 'CS'
ORDER BY id
LIMIT 10;
```

觀察 PostgreSQL 實際查詢效能。

### 7. 資安重點

### 7.1 SQL Injection

錯誤：
```python
sql = f"SELECT * FROM courses WHERE name = '{keyword}'"
```

攻擊者可能輸入惡意 SQL，改變原本查詢邏輯。正確：
```python
cur.execute(
  "SELECT * FROM courses WHERE name = %s",
  (keyword,)
)
```

使用 Parameterized Query（參數化查詢）。

**注意：SQL 參數只能用於資料值，不能直接替代資料表名稱或欄位名稱。**

動態排序欄位應使用白名單：
```python
allowed_sort = {
  "id": "id",
  "name": "name",
  "credits": "credits"
}

sort_column = allowed_sort.get(sort_by, "id")
```

#### 7.2 Pagination 限制

```python
size: int = Query(10, ge=1, le=100)
```

限制每頁最多 100 筆，避免使用者一次要求過多資料。但這不能完全防止大量查詢造成的負載，仍需考慮 Rate Limiting、Timeout 等措施。

#### 7.3 VIEW 不等於完整的資料安全機制

VIEW 可以配合資料庫權限，限制應用程式能讀取的資料欄位。例如不暴露敏感資料：
```sql
CREATE VIEW v_public_members AS
SELECT id, display_name
FROM members;
```

仍需注意：
- VIEW Owner 與 Invoker 的權限語意。
- PostgreSQL 版本及 `security_invoker` 設定。
- Row-Level Security（RLS）政策。
- 不可單靠 VIEW 取代 API Authentication / Authorization。

### 8. 進階：OFFSET vs. Keyset Pagination

#### OFFSET Pagination
```sql
SELECT *
FROM courses
ORDER BY id
LIMIT 10 OFFSET 100000;
```
- 優點：容易跳到指定頁碼。
- 缺點：OFFSET 很大時，資料庫可能需要處理大量前面的資料列。

### Keyset Pagination（Cursor-based）
```sql
SELECT *
FROM courses
WHERE id > 1000
ORDER BY id
LIMIT 10;
```

利用上一頁最後一筆 ID 作為下一頁的起點。優點：
- 適合大量資料與無限捲動。
- 搭配適當索引，通常能改善深度分頁效能。
- 對新增或刪除資料造成的頁面位移較不敏感。

缺點：
- 不容易直接跳到第 N 頁。
- 複合排序時需要設計對應 Cursor。

### 9. AI Coding 實作練習

#### Task 1：基本查詢

使用 AI 協助完成：
```http
GET /courses?page=2&size=5
```

要求：
- 正確計算 OFFSET。
- 回傳 total、total_pages。
- 固定排序，避免分頁順序不穩定。

#### Task 2：動態篩選與搜尋

加入：
```http
GET /courses?department=CS&keyword=Web
```

檢查：
- 未提供參數時能否正常查詢？
- 多個條件是否使用 AND？
- keyword 為空字串時如何處理？
- SQL 是否使用 Parameterized Query？

#### Task 3：VIEW 重構
要求 AI：
> 將課程查詢中重複使用的 JOIN 與固定條件抽離至 PostgreSQL VIEW，保留 FastAPI 的動態篩選、搜尋、分頁及 JSON 回應格式。比較重構前後的 SQL 與程式碼。

#### Task 4：效能分析

使用：
```sql
EXPLAIN (ANALYZE, BUFFERS)
```

比較：
1. 直接查詢 TABLE。
2. 查詢 VIEW。
3. 加入 Index 後的查詢。

不要只相信 AI 說「VIEW 比較快」，應以實際執行計畫及測量結果驗證。

### 10. AI 學習心得（ai.md）

請學生回答：
1. AI 產生的 SQL 如何避免 SQL Injection？
2. 為何 VIEW 不一定比直接查詢 TABLE 快？
3. 哪些查詢邏輯適合放在 VIEW，哪些適合放在 FastAPI？
4. 當資料量增加到 100 萬筆時，OFFSET Pagination 可能發生什麼問題？
5. 本週 AI 產生的程式碼中，自己發現、修正或驗證了哪些問題？

#### 本週筆記（足弓／objectlist）

1. **AI 產生的 SQL 如何避免 SQL Injection？**  
   使用者輸入（如 `q`）只當 **參數值** 傳給 psycopg（`%s`），不要用 f-string 把 keyword 拼進 SQL 本文。動態組的只有「要不要加這段條件」；欄位名若動態必須白名單。本週 `list_by_cid_page`：`ILIKE %s`，`'%' + keyword + '%'` 放在 params。

2. **為何 VIEW 不一定比直接查詢 TABLE 快？**  
   一般 VIEW 是存起來的查詢定義，執行時仍會展開打底表，再由規劃器決定計畫。不會自動比較快；複雜 VIEW 甚至多一層。快不快看索引與 `EXPLAIN (ANALYZE, BUFFERS)`，不能只信「用了 VIEW」。

3. **哪些適合 VIEW，哪些適合 FastAPI？**  
   - VIEW：固定 JOIN、穩定欄位、重複語意（`vd_objectlist`＝co＋object＋縮圖欄）。  
   - FastAPI：每次不同的 `q`／`page`／`size`、權限、Pydantic 驗證、組 `{total, total_pages}` JSON。  
   VIEW 不會自動分頁或動態 keyword。

4. **100 萬筆時 OFFSET 可能怎樣？**  
   `OFFSET` 很大時，DB 常仍要跳過前面大量列，越深越慢；中間增刪資料也可能讓同一頁號內容位移。大量＋無限捲動較常用 Keyset（`WHERE oid > last ORDER BY oid LIMIT n`）。

5. **自己發現／修正／驗證了什麼？**  
   - 曾做自訂 `/api/exercise/search`，偏離 reuse `vd_subclass`／objectlist → 改回 VIEW＋既有端點。  
   - API 改回傳 `{items,total,page,size,total_pages}` 後前端要跟著改，不能再當純陣列。  
   - 關鍵字曾只前端過濾 → 補參數化 `ILIKE`，用 `q=提踵`、`page=2&size=5` 對過 total。  
   - 多目錄 AND 仍多次 objectlist 交集：當小資料取捨，不是十萬筆級做法。

GitHub Commit 建議：
```text
feat: add course pagination
feat: support dynamic filtering and keyword search
refactor: extract course query into PostgreSQL view
test: verify pagination and search edge cases
docs: document query performance and AI review
```

每個 Commit 應對應實際且可驗證的程式變更，而不是為增加 Commit 數量刻意拆分。

### 11. 結論與建議

實務上建議採取 **FastAPI + PostgreSQL VIEW 混合架構**：

| 職責 | 建議位置 |
|---|---|
| HTTP Query Parameters | FastAPI |
| 參數驗證 | FastAPI / Pydantic |
| Authentication | FastAPI |
| Authorization | FastAPI + DB |
| 動態 Filtering | FastAPI 傳條件，PostgreSQL 執行 |
| Searching | PostgreSQL SQL / Index |
| Pagination | FastAPI 計算，PostgreSQL 執行 |
| 複雜 JOIN | PostgreSQL VIEW |
| 共用資料查詢定義 | PostgreSQL VIEW |
| JSON Response | FastAPI |
| Query Optimization | PostgreSQL Index / EXPLAIN |

---

## W10：錯誤處理、Logging、Middleware {#logging}
看訊息，思考logs該如何做？
```text
PS C:\code\psql\api> & c:/code/psql/api/venv/Scripts/Activate.ps1
(venv) PS C:\code\psql\api> .\run.bat

C:\code\psql\api>uvicorn app.main:app --reload --host 0.0.0.0 --port 7777 
INFO:     Will watch for changes in these directories: ['C:\\code\\psql\\api']
INFO:     Uvicorn running on http://0.0.0.0:7777 (Press CTRL+C to quit)
INFO:     Started reloader process [15524] using WatchFiles
INFO:     Started server process [15716]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     163.22.22.45:64686 - "GET /api/subclass/pcid/249 HTTP/1.1" 200 OK
INFO:     163.22.22.45:64687 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:64689 - "GET / HTTP/1.1" 304 Not Modified
INFO:     163.22.22.45:64689 - "GET /js/records.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:64689 - "GET /api/auth/me HTTP/1.1" 200 OK
INFO:     163.22.22.45:64690 - "GET /api/root HTTP/1.1" 200 OK
INFO:     163.22.22.45:64689 - "GET /api/subclass/pcid/249 HTTP/1.1" 200 OK
INFO:     163.22.22.45:64690 - "GET /api/root/co/25 HTTP/1.1" 200 OK
INFO:     163.22.22.45:64690 - "GET /api/subclass/pcid/251 HTTP/1.1" 200 OK
INFO:     163.22.22.45:64690 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57205 - "GET /api/root/co/261 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57207 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57210 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57212 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57212 - "GET /api/docs HTTP/1.1" 200 OK
INFO:     163.22.22.45:57212 - "GET /api/openapi.json HTTP/1.1" 200 OK
INFO:     163.22.22.45:57214 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57222 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57223 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57228 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57229 - "GET / HTTP/1.1" 200 OK
INFO:     163.22.22.45:57229 - "GET /css/style.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57230 - "GET /js/app.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57229 - "GET /css/responsive.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57231 - "GET /css/components.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57232 - "GET /css/layout.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57230 - "GET /js/api.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57234 - "GET /js/sidebar.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57233 - "GET /js/account.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57237 - "GET /js/data-view.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57236 - "GET /js/dashboard.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57235 - "GET /js/navigation.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57232 - "GET /js/records.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57229 - "GET /js/data-table.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57237 - "GET /favicon.svg HTTP/1.1" 200 OK
INFO:     163.22.22.45:57235 - "GET /api/auth/me HTTP/1.1" 200 OK
INFO:     163.22.22.45:57231 - "GET /api/root HTTP/1.1" 200 OK
INFO:     163.22.22.45:57234 - "GET /api/subclass/pcid/249 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57230 - "GET /api/subclass/pcid/251 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57229 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57238 - "GET /api/root/co/1964 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57239 - "GET /api/root/co/2072 HTTP/1.1" 200 OK
INFO:     10.21.26.181:61038 - "GET /s115999999/api/root/co/2072 HTTP/1.1" 200 OK
INFO:     10.21.26.181:61612 - "GET /s115999999/api/root/co/2072 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57243 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57243 - "GET /api/root/co/1946 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57244 - "GET /api/root/co/2304 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57245 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57245 - "GET /api/root/co/1954 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57246 - "GET /api/root/co/260 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57246 - "GET /api/root/co/1954 HTTP/1.1" 200 OK
INFO:     10.21.26.181:61888 - "GET /s115999999/api/root/co/1954 HTTP/1.1" 200 OK
INFO:     163.22.22.45:57247 - "GET / HTTP/1.1" 200 OK
INFO:     163.22.22.45:57247 - "GET /js/app.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57248 - "GET /css/style.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57249 - "GET /js/api.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57247 - "GET /js/account.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57251 - "GET /js/navigation.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57250 - "GET /js/sidebar.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57252 - "GET /js/dashboard.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57253 - "GET /js/data-view.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57248 - "GET /css/layout.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57255 - "GET /css/components.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57254 - "GET /css/responsive.css HTTP/1.1" 200 OK
INFO:     163.22.22.45:57249 - "GET /js/data-table.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57247 - "GET /js/records.js HTTP/1.1" 200 OK
INFO:     163.22.22.45:57251 - "GET /favicon.svg HTTP/1.1" 200 OK
```

### 1. 學習目標
建立FastAPI統一錯誤處理機制，並透過PostgreSQL記錄API執行狀態。
- Exception Handling：統一處理HTTP及程式執行錯誤。
- Middleware：攔截Request/Response，記錄執行資訊。
- Structured Logging：以結構化資料儲存Log。
- Session Tracking：追蹤使用者Session及相關API操作。
- Asynchronous Logging：API回應與Log寫入分離。
- Security：避免Log洩漏敏感資訊。

核心問題：
> 如何讓API發生錯誤時，Client收到一致的錯誤格式，同時由Server非同步記錄至PostgreSQL，而不明顯影響API回應時間？

### 2. 系統架構
```text
Client (Browser / React)
          |
          | HTTP Request
          v
FastAPI Middleware
  ├── 產生 Request ID
  ├── 辨識 Session ID
  └── 開始計時
          |
          v
FastAPI Endpoint
  ├── 正常執行
  └── 發生錯誤
        |
        v
   Exception Handler
   └── 統一錯誤 JSON
          |
          v
FastAPI Middleware
  ├── HTTP Status
  ├── Duration
  ├── Error Code
  └── Structured Log
          |
          +----------------------+
          |                      |
          v                      v
    HTTP Response          Background Task
    回傳 Client                  |
                                 v
                             PostgreSQL
                         api_sessions (1)
                               |
                               | 1:N
                               v
                           api_logs (N)
```

設計原則：
1. API不應等待Log寫入資料庫後才回應。
2. 每個Request都有唯一Request ID。
3. 同一Session可對應多筆API Logs。
4. 所有HTTP錯誤使用一致的JSON格式。
5. Log儲存必要資訊，不包含敏感資料。

注意：FastAPI BackgroundTasks在Response送出後執行，但仍屬於同一應用程式進程，不保證Log一定成功寫入。

### 3. PostgreSQL資料表設計

#### 3.1 Session Table
```text
瀏覽器 Cookie
api_session = UUID + 時間戳記 + 簽章
                    ↓
每次請求自動帶給 FastAPI
                    ↓
Middleware 驗證簽章，取出 UUID
                    ↓
對應 PostgreSQL 的 api_sessions.id
```

Session代表使用者的一次應用程式工作階段。
```sql
CREATE TABLE IF NOT EXISTS api_sessions (
	id UUID PRIMARY KEY,
	mid INTEGER,
	ip INET,
	started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	ended_at TIMESTAMPTZ
);
```

欄位說明：
| 欄位 | 說明 |
|---|---|
| id | Session唯一識別碼 |
| member_id | 使用者ID，可為NULL |
| ip | 可儲存 IPv4、IPv6；若要追蹤每次請求的 IP，應另外記錄在 request log。 |
| started_at | Session建立時間 |
| last_seen_at | 最近活動時間 |
| ended_at | Session結束時間 |

Session ID應由Server產生，並透過可信任的Session或Authentication機制驗證。不要將原始JWT或Session Token直接存入Log。

#### 3.2 Log Table
一個Session可包含多筆API操作紀錄。
```sql
CREATE TABLE api_logs (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  session_id UUID REFERENCES api_sessions(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ip INET,
  method VARCHAR(10) NOT NULL,
  path TEXT NOT NULL,
  status_code INTEGER NOT NULL,
  message TEXT
);
```

建立Index：
```sql
-- 依時間範圍查詢、查看最新紀錄
CREATE INDEX idx_api_logs_created_at ON api_logs (created_at);
-- 查詢某個 session 的紀錄，並依時間排序
CREATE INDEX idx_api_logs_session_created_at ON api_logs (session_id, created_at);
-- 依 IP 查詢，並依時間排序
CREATE INDEX idx_api_logs_ip_created_at ON api_logs (ip, created_at);
```
```sql
-- Session：建立、查詢與更新最後活動時間
GRANT SELECT, INSERT, UPDATE ON TABLE public.api_sessions TO dev_user;
-- Log：新增紀錄
GRANT INSERT ON TABLE public.api_logs TO dev_user;
-- Log 自動編號需要使用 sequence
-- GRANT USAGE ON SEQUENCE public.api_logs TO dev_user;
```

思考上述SQL會建立在哪個Schema？

```sql
CREATE TABLE IF NOT EXISTS public.api_sessions (
    id UUID PRIMARY KEY,
    mid INTEGER,
    ip INET,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS public.api_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id UUID REFERENCES public.api_sessions(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip INET,
    method VARCHAR(10) NOT NULL,
    path TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    message TEXT
);
CREATE INDEX IF NOT EXISTS idx_api_logs_created_at ON public.api_logs (created_at);
CREATE INDEX IF NOT EXISTS idx_api_logs_session_created_at ON public.api_logs (session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_api_logs_ip_created_at ON public.api_logs (ip, created_at);
GRANT SELECT, INSERT, UPDATE ON TABLE public.api_sessions TO dev_user;
GRANT INSERT ON TABLE public.api_logs TO dev_user;
```

#### 3.3 EER Relationship
```text
api_sessions
-----------------------
PK id
   member_id
   started_at
   last_seen_at
   ended_at
         |
         | 1
         |
         | N
         v
api_logs
-----------------------
PK id
FK session_id
   request_id
   created_at
   level
   method
   path
   status_code
   duration_ms
   error_code
   message
   details
```

關聯：
- 一個Session可以有多筆Logs。
- 每筆Log最多屬於一個Session。
- 匿名請求的session_id可以為NULL。
- request_id用於追蹤單一HTTP請求。

### 4. 統一錯誤回應格式
所有API錯誤使用一致JSON格式：
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "找不到指定資源"
  },
//   "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```
- `request_id` 將來可用於識別一連串操作，log records對應相同request_id

常見HTTP錯誤：
| Status | Error Code | 說明 |
|---|---|---|
| 400 | BAD_REQUEST | 請求格式錯誤 |
| 401 | UNAUTHORIZED | 尚未通過身分驗證 |
| 403 | FORBIDDEN | 權限不足 |
| 404 | NOT_FOUND | 資源不存在 |
| 422 | VALIDATION_ERROR | 參數驗證失敗 |
| 500 | INTERNAL_ERROR | 伺服器內部錯誤 |

重要原則：
- Client收到簡潔且安全的錯誤訊息。
- Server Log保留必要的診斷資訊。
- 不應回傳Traceback、SQL錯誤細節或資料庫連線資訊。

### 5. FastAPI實作

> 根據設計，讓fastapi加入非同步session and log與錯誤處理處理，以middleware 非同步寫入PostgreSQL

```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 7777 --loop app.core.event_loop:selector_loop_factory
```

#### 為什麼修改 run.bat？

讓 FastAPI **非同步寫入 PostgreSQL**。「非同步」表示：當程式等待資料庫回覆時，FastAPI 可以先處理其他工作，不必停在原地等。Python 需要一個「工作調度員」來安排這些工作，這就是 **event loop（事件迴圈）**。

#### Windows 的事件迴圈

Windows 有兩種 event loop：

| 種類 | psycopg 非同步連線能否使用 |
|---|---|
| ProactorEventLoop | 不支援 |
| SelectorEventLoop | 支援 |

所以在 `run.bat` 的啟動指令加上：

```bat
--loop app.core.event_loop:selector_loop_factory
```

這段可以拆成：

- `--loop`：指定使用哪個事件迴圈。
- `app.core.event_loop`：找到專案的 `app/core/event_loop.py`。
- `selector_loop_factory`：呼叫這個檔案裡的函式。

#### 函式內容

```python
import asyncio


def selector_loop_factory():
    return asyncio.SelectorEventLoop()
```

意思就是：「建立一個 psycopg 可以使用的工作調度員。」

修改 `run.bat` 的目的，是讓 Windows 使用相容的執行方式，確保 session 和 log 能非同步寫入資料庫。原本一般同步的資料庫操作不需要這個設定。

`--loop app.core.event_loop:selector_loop_factory` 會讓 Uvicorn 使用 SelectorEventLoop。Windows 預設的 ProactorEventLoop 不支援 psycopg 的非同步連線，可能導致 session、log 寫入失敗。

你目前的 --reload 模式通常已使用 Selector，因此這個參數主要是明確固定設定，避免移除 --reload 後出問題。

#### 5.1 安裝套件
```bash
pip install fastapi uvicorn "psycopg[binary]"
```

設定環境變數：
```text
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

實務上應透過環境變數或Secrets Manager管理連線資訊，不要將密碼提交至GitHub。

#### 5.2 非同步寫入PostgreSQL
建立`app/logging_db.py`：

```python
import os
import logging
import psycopg

logger = logging.getLogger("api")
DATABASE_URL = os.environ["DATABASE_URL"]

async def save_log(data):
  try:
    async with await psycopg.AsyncConnection.connect(
      DATABASE_URL
    ) as conn:
      async with conn.cursor() as cur:
        await cur.execute("""
          INSERT INTO api_logs (
            session_id,
            request_id,
            level,
            method,
            path,
            status_code,
            duration_ms,
            error_code,
            message
          )
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
          data["session_id"],
          data["request_id"],
          data["level"],
          data["method"],
          data["path"],
          data["status_code"],
          data["duration_ms"],
          data["error_code"],
          data["message"]
        ))

  except Exception:
    logger.exception("Failed to save API log")
```

使用Parameterized Query防止SQL Injection。注意：
- `async def`允許在等待I/O時讓出執行權。
- 非同步不等於平行執行。
- 每次建立資料庫連線會有額外成本。
- 正式系統建議使用Connection Pool。

### 6. Exception Handler
建立`app/main.py`：
```python
import uuid
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import (
  HTTPException as StarletteHTTPException
)

app = FastAPI()
logger = logging.getLogger("api")

def error_response(request, status, code, message):
  request.state.error_code = code
  request.state.error_message = message

  return JSONResponse(
    status_code=status,
    content={
      "success": False,
      "error": {
        "code": code,
        "message": message
      },
      "request_id": str(request.state.request_id)
    }
  )

@app.exception_handler(StarletteHTTPException)
async def http_error(request, exc):
  return error_response(
    request,
    exc.status_code,
    f"HTTP_{exc.status_code}",
    str(exc.detail)
  )

@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
  return error_response(
    request,
    422,
    "VALIDATION_ERROR",
    "請求參數驗證失敗"
  )

@app.exception_handler(Exception)
async def unexpected_error(request, exc):
  logger.error(
    "Unhandled error: request_id=%s",
    getattr(request.state, "request_id", "unknown"),
    exc_info=(type(exc), exc, exc.__traceback__)
  )

  return error_response(
    request,
    500,
    "INTERNAL_ERROR",
    "伺服器內部錯誤"
  )
```

Exception Handler的用途：
1. 將不同錯誤轉換成一致的JSON格式。
2. 避免將內部錯誤細節暴露給Client。
3. 讓Frontend可以依error.code進行處理。

### 7. Middleware + Background Logging
在`app/main.py`加入：
```python
import time
from fastapi import BackgroundTasks
from app.logging_db import save_log

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
  start = time.perf_counter()

  request.state.request_id = uuid.uuid4()
  request.state.error_code = None
  request.state.error_message = None

  # 示範匿名請求。
  # 登入後應由可信任的Session機制取得。
  request.state.session_id = None

  try:
    response = await call_next(request)

  except Exception:
    logger.exception(
      "Request failed: %s",
      request.state.request_id
    )

    response = error_response(
      request,
      500,
      "INTERNAL_ERROR",
      "伺服器內部錯誤"
    )

  duration = (time.perf_counter() - start) * 1000
  status = response.status_code

  level = (
    "ERROR" if status >= 500
    else "WARNING" if status >= 400
    else "INFO"
  )

  log_data = {
    "session_id": request.state.session_id,
    "request_id": request.state.request_id,
    "level": level,
    "method": request.method,
    "path": request.url.path,
    "status_code": status,
    "duration_ms": duration,
    "error_code": request.state.error_code,
    "message": request.state.error_message
  }

  tasks = BackgroundTasks()
  tasks.add_task(save_log, log_data)

  response.background = tasks

  response.headers["X-Request-ID"] = str(
    request.state.request_id
  )

  return response
```

執行流程：
```text
1. Client發送HTTP Request
2. Middleware產生Request ID
3. Endpoint執行
4. Exception Handler處理預期錯誤
5. Middleware計算Duration
6. 建立Structured Log
7. HTTP Response回傳Client
8. BackgroundTasks寫入PostgreSQL
```

此程式為教學簡化版本。注意：
- 直接設定`response.background`可能覆蓋既有Background Tasks。
- 未預期例外可能在Middleware與Exception Handler重複記錄。
- Streaming Response的完成時間與錯誤處理需要額外設計。
- BackgroundTasks不保證Log持久化。
- 真正需要高可靠度的稽核Log，應使用Message Queue與獨立Worker。或是和業務資料放在同一個資料庫 transaction 中提交。

### 8. API測試
加入測試Endpoint：
```python
@app.get("/courses/{course_id}")
async def get_course(course_id: int):
  if course_id == 0:
    raise HTTPException(
      status_code=404,
      detail="Course not found"
    )

  if course_id == 999:
    raise RuntimeError("Simulated server failure")

  return {
    "id": course_id,
    "name": "Web Programming"
  }
```

啟動：
```bash
uvicorn app.main:app --reload
```

測試：
```http
GET /courses/1
GET /courses/0
GET /courses/999
GET /courses/abc
```

預期：
| Request | HTTP Status | Log Level |
|---|---|---|
| /courses/1 | 200 | INFO |
| /courses/0 | 404 | WARNING |
| /courses/999 | 500 | ERROR |
| /courses/abc | 422 | WARNING |

驗證：
- Client是否收到統一JSON？
- 每筆Request是否產生唯一Request ID？
- PostgreSQL是否正確記錄Status？
- 是否記錄執行時間？
- 發生500錯誤時，是否避免洩漏內部資訊？

### 9. PostgreSQL Log查詢

#### 9.1 最近20筆API紀錄

```sql
SELECT
  request_id,
  level,
  method,
  path,
  status_code,
  duration_ms,
  created_at
FROM api_logs
ORDER BY created_at DESC
LIMIT 20;
```

#### 9.2 查詢錯誤紀錄

```sql
SELECT *
FROM api_logs
WHERE status_code >= 400
ORDER BY created_at DESC;
```

#### 9.3 統計各API錯誤數量

```sql
SELECT
  path,
  status_code,
  COUNT(*) AS error_count
FROM api_logs
WHERE status_code >= 400
GROUP BY path, status_code
ORDER BY error_count DESC;
```

#### 9.4 統計API平均執行時間

```sql
SELECT
  path,
  COUNT(*) AS requests,
  ROUND(AVG(duration_ms)::numeric, 2) AS avg_ms
FROM api_logs
GROUP BY path
ORDER BY avg_ms DESC;
```

#### 9.5 查詢Session操作紀錄

```sql
SELECT
  s.id AS session_id,
  l.request_id,
  l.method,
  l.path,
  l.status_code,
  l.created_at
FROM api_sessions s
JOIN api_logs l
  ON s.id = l.session_id
WHERE s.id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY l.created_at;
```

注意：目前API範例尚未實作Session建立與驗證，因此Log的session_id為NULL。完成Session整合後，才會出現1:N關聯資料。

### 10. Security Considerations

#### 10.1 不應記錄的資訊
- Password
- JWT Access Token
- Refresh Token
- Session Cookie
- Authorization Header
- API Key
- 個人敏感資料
- 完整SQL錯誤與資料庫連線密碼

#### 10.2 Log Injection

使用者可能在輸入內容加入換行或控制字元，影響Log閱讀與分析。建議：
- 使用結構化JSON Log。
- 限制可記錄的欄位。
- 不直接記錄完整Request Body。
- 對不可信任字串進行長度限制與必要的清理。

#### 10.3 Log Retention

Log不應無限期保存。應根據系統需求設定：
- 保存期限。
- 存取權限。
- 定期清除或封存。
- 資料庫容量監控。

#### 10.4 Session Security
Session ID不等於Authentication。應注意：
- Session ID必須不可預測。
- Server應驗證Session有效性。
- Session應設定過期時間。
- 登出後應使Session失效。
- 不可直接信任Client傳入的Session ID。

### 11. BackgroundTasks vs. Message Queue

| 比較 | FastAPI BackgroundTasks | Message Queue + Worker |
|---|---|---|
| 實作難度 | 低 | 較高 |
| 額外服務 | 不需要 | 通常需要 |
| API回應後執行 | 支援 | 支援 |
| 獨立Process | 否 | 可以 |
| 持久化Queue | 無 | 視系統設計 |
| Retry機制 | 需自行實作 | 通常可配置 |
| 進程中斷風險 | 可能遺失Log | 可降低遺失風險 |
| 適用情境 | 教學、非關鍵Log | 大型系統、重要稽核紀錄 |

注意：BackgroundTasks雖然可以在Response送出後執行，但不等於可靠的非同步工作佇列。若Log屬於資安稽核紀錄，應考慮可靠的持久化機制、Retry及失敗告警。

### 12. AI Coding實作練習

#### Task 1：Exception Handling
Prompt：
> 請協助FastAPI建立統一Exception Handler，處理HTTPException、RequestValidationError與未預期的Exception，回傳一致JSON格式。500錯誤不得暴露Traceback或SQL細節。

#### Task 2：Middleware
Prompt：
> 請建立FastAPI Middleware，為每個HTTP Request產生UUID Request ID，計算執行時間，並記錄HTTP Method、Path、Status Code與Duration。

#### Task 3：PostgreSQL Logging
Prompt：
> 請建立PostgreSQL api_sessions與api_logs資料表，使用1:N關聯，並透過psycopg 3的AsyncConnection寫入Structured Log。所有SQL必須使用Parameterized Query。

#### Task 4：Background Logging
Prompt：
> 請使用FastAPI BackgroundTasks，在HTTP Response送出後非同步寫入PostgreSQL。當資料庫寫入失敗時，不得造成已完成的API Response失敗，並說明此設計可能遺失Log的情況。

#### Task 5：Security Review
Prompt：
> 請從OWASP安全性角度檢查FastAPI Logging系統，包括Sensitive Data Exposure、Log Injection、Session Hijacking及Log存取權限，指出問題並提出修正方式。

### 13. ai.md學習心得

學生需回答：

1. Middleware與Exception Handler有何差異？
2. 為何需要Request ID與Session ID兩種識別碼？
3. `async def`與BackgroundTasks有何不同？
4. BackgroundTasks是否保證Log一定成功寫入？
5. 為何不應記錄JWT、Cookie與Password？
6. 如果PostgreSQL暫時無法連線，API與Logging各會發生什麼情況？
7. AI產生的Logging程式碼有哪些潛在資安問題？

#### 本週筆記（足弓／錯誤處理與 Logging）

（與 `ai.md` W10 同一套；細節實作見該週完成項。）

1. **Middleware vs Exception Handler**  
   Middleware 包住整段請求（進出都經過，適合計時、記 log）。Handler 只在丟出例外時接手，負責統一錯誤 JSON。

2. **為何要 Request ID 與 Session ID**  
   Request ID＝這一發 HTTP 的追蹤碼（串 log）。Session／登入態＝同一使用者跨多次請求。講義完整版兩者都有；本專案主要靠 JWT cookie 認人，請求 log 記 method／path／status／耗時。

3. **`async def` vs BackgroundTasks**  
   `async def`＝請求處理中可 await I/O，仍在回應完成前。BackgroundTasks＝回應先送出後再跑，不擋使用者拿到結果。

4. **BackgroundTasks 保證 Log 寫成功？**  
   **不保證。** 程序／DB 掛掉或任務失敗都可能丟 log，API 卻可能已 200。稽核級 log 要佇列／重試／告警。

5. **為何不記 JWT、Cookie、Password**  
   Log 常被多人看或進檔案；寫進去等於洩漏通行證與密碼。只記路徑、狀態、耗時等必要欄。

6. **PostgreSQL 暫時連不上**  
   依賴 DB 的 API 會失敗（錯誤 JSON／500）。若 log 也寫 PG 且在關鍵路徑，連 log 都可能失敗；BackgroundTasks 寫 log 時 API 仍可能先成功但 log 遺失。本專案目前 log 多半寫 `logs/app.log`，DB 掛了仍可能留下檔案 log。

7. **AI Logging 常見資安問題**  
   把 header／body／token 整段打進 log；字串拼 SQL；對外 500 回 traceback；log 檔可被網頁下載；缺少存取權限控管。

建議Git Commit：

```text
feat: add unified exception handling
feat: add request logging middleware
feat: create PostgreSQL session and log tables
feat: implement asynchronous background logging
test: verify error responses and logging behavior
docs: document logging security review
```

### 14. W10重點整理

| 功能 | 技術 | 責任 |
|---|---|---|
| HTTP錯誤處理 | Exception Handler | 統一錯誤格式 |
| Request攔截 | Middleware | 追蹤Request |
| Request識別 | UUID | 單一請求追蹤 |
| Session識別 | Session ID | 使用者工作階段追蹤 |
| 結構化紀錄 | PostgreSQL JSONB | 儲存Log資料 |
| 非同步寫入 | BackgroundTasks | 減少回應等待 |
| 資料庫操作 | psycopg AsyncConnection | 非同步DB I/O |
| 安全防護 | Parameterized Query | 防止SQL Injection |
| 效能分析 | SQL Aggregation | 分析API錯誤率與延遲 |

### 核心觀念

**Exception Handler負責錯誤回應，Middleware負責Request追蹤，PostgreSQL負責Log持久化，BackgroundTasks負責將非關鍵Log寫入工作移至Response之後。**

AI Coding的重點是理解各元件的責任、驗證非同步行為，並確認Logging機制不會引入新的資安風險。


---

## W11：Docker 化 {#Docker}

### 學習目標
把 FastAPI + PostgreSQL 用 docker-compose 一鍵啟動。

### 操作步驟

`Dockerfile`：
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip Install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`docker-compose.yml`：
```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_Member: dev_Member
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: FastAPI_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdaTa:/var/lib/postgresql/daTa

  api:
    build: .
    depends_on:
      - db
    environment:
      Database_URL: postgresql://dev_Member:dev_password@db:5432/FastAPI_dev
    ports:
      - "8000:8888"

volumes:
  pgdaTa:
```

啟動：
```bash
docker compose up --build
```

### 本週練習
1. 確認容器重啟後資料還在（驗證 volume 是否正確掛載）
2. 加入 migration 自動執行的步驟（在 `api` 容器啟動時先跑 `alembic upgrade head`）
3. 研究並寫下：production 環境下，為什麼不建議用 `--reload`，也不建議把資料庫密碼寫死在 `docker-compose.yml`

### 驗收標準
- [ ] `docker compose up` 後，API 與資料庫都能正常運作且互通
- [ ] 重啟容器後資料不遺失

---

## W12：部署與整合專題 {#deploy}

### 學習目標
把前 11 週的成果整合成一個完整、可展示的後端專案，並理解基本部署概念。

### 本週任務（作為期末專題，不提供完整程式碼，靠你自己整合）

1. **功能整合**：確認 CRUD、關聯查詢、Auth、分頁搜尋、錯誤處理、Logging 全部串在同一個專案中並能正常運作
2. **文件補齊**：撰寫一份 `README.md`，說明專案架構、如何啟動、API 一覽（可搭配 `/docs` 的 Swagger UI）
3. **CI 基礎**：用 GitHub Actions 設定一個簡單的 workflow，每次 push 自動執行 `pytest`
4. **部署嘗試**（擇一）：
   - 部署到 Render / Railway 等平台的免費方案
   - 或在自己的雲端主機用 docker-compose 跑起來
5. **架構回顧**：以你的 software architect 背景，寫一頁簡短的技術筆記，評估這個專案目前的**架構限制**（例如：沒有 rate limiting、沒有 cache layer、沒有背景任務佇列），並列出如果要正式上線，你會優先補強哪三項

### 驗收標準
- [ ] 專案可以從乾淨環境（新 clone 下來）依照 README 步驟成功啟動
- [ ] CI 能在 push 時自動跑測試並回報結果
- [ ] 完成架構限制評估筆記

---

## 學習方式提醒

每週的「本週練習」請自己動手寫，卡住時可以帶著具體錯誤訊息來討論，而不是直接要完整程式碼——這樣 12 週後你會真正掌握這套技術棧的操作邏輯，而不只是有一份能跑的程式碼。


-------------------------------------------------------------
## W7：測試（pytest）{#pytest}

用 pytest + FastAPI TestClient 對 CRUD 與 Auth 寫自動化測試。

### 操作步驟

```bash
pip Install pytest httpx
```

`tests/conftest.py`（用獨立測試資料庫，避免污染開發資料）：
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from FastAPI.testclient import TestClient
from app.main import app
from app.core.Database import Base, get_db

TEST_Database_URL = "postgresql://dev_Member:dev_password@localhost:5432/FastAPI_test"
engine = create_engine(TEST_Database_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.meTadaTa.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.meTadaTa.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
```

`tests/test_notes.py`：
```python
def test_create_note(client):
    response = client.post("/notes/", json={"title": "test", "content": "hello"})
    assert response.Status_code == 200
    assert response.json()["title"] == "test"

def test_get_nonexistent_note(client):
    response = client.get("/notes/999")
    assert response.Status_code == 404
```

### 本週練習
1. 為 `/register` 與 `/login` 寫測試（含密碼錯誤情境）
2. 為「使用者不能刪除別人的 note」這個規則寫一個測試
3. 執行 `pytest -v`，確保全部通過

### 驗收標準
- [ ] 測試覆蓋所有 CRUD 端點與主要錯誤情境
- [ ] `pytest` 全數通過，且測試資料庫不影響開發資料庫

### 本週筆記（足弓專案）
- 無密碼 `/register`／`/login`：改測 JWT 門禁（401）＋ notes CRUD；「不能動別人資料」改測 scan 404／401。
- `tests/`：`conftest` 的 `auth_client` 用 `dependency_overrides` 假裝登入；`pytest -v` 已通過。
- **資安**：override **只在跑 pytest 的行程內**有效，不是對外後門。線上 uvicorn 仍驗真 JWT，沒票還是 401。

---

## W8：非同步與連線池 {#pools}

### 學習目標
理解 FastAPI 的 async 支援，並改用 async ORM 操作。

### 為什麼這樣安排
你熟悉 Node.js 的非同步模型，這週會對照講解 Python 的 `async/await` 跟 Node 的 event loop 概念異同，並說明「不是所有東西都要 async」的判斷原則。

### 操作步驟

```bash
pip Install asyncpg "sqlalchemy[asyncio]"
```

`app/core/Database.py`（改為 async engine）：
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

ASYNC_Database_URL = "postgresql+asyncpg://dev_Member:dev_password@localhost:5432/FastAPI_dev"
engine = create_async_engine(ASYNC_Database_URL, pool_size=10, max_overflow=20)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

改寫端點為 async：
```python
from sqlalchemy import select

@router.get("/", response_model=list[NoteResponse])
async def list_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note))
    return result.scalars().all()
```

### 本週練習
1. 把 W4-W6 的所有端點改寫為 async 版本
2. 用 `pool_size` 與 `max_overflow` 參數，理解連線池的上限概念（對應你熟悉的資料庫連線池概念，例如 HikariCP）
3. 寫一個簡單的負載測試（可用 `locust` 或手動並發請求），比較 sync 與 async 版本在高並發下的差異

### 驗收標準
- [ ] 所有端點改為 async 且功能不變
- [ ] 能解釋「什麼情境下 async 才真的有幫助」（I/O bound vs CPU bound）

### 本週筆記
- 講義是 SQLAlchemy async＋asyncpg；本專案留 **psycopg**，改接 `psycopg_pool`。
- **同步池**：`get_connection()` → `ConnectionPool`（scan／member／subclass 沿用）。
- **非同步池**：notes 改 `async def` + `AsyncConnectionPool`（示範真 await DB）。
- 池大小：`DB_POOL_MIN_SIZE`／`DB_POOL_MAX_SIZE`（對應講義 `pool_size`／`max_overflow` 觀念）。
- **何時 async 有用**：等 DB／網路（I/O）時可交錯處理請求；SAM／重 CPU 仍不該塞進 API event loop（繼續放 worker）。
- 並發：`tests/test_pool_concurrent.py`；啟動時 `main.py` lifespan 開關池。
- Windows：psycopg async 不能用 ProactorEventLoop，`main.py`／`conftest.py` 改 `WindowsSelectorEventLoopPolicy`。