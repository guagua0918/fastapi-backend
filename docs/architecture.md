# 目前程式架構（W04 notes）

一次 notes 請求的方向：

```text
瀏覽器 / Swagger
  → app/main.py              建立 FastAPI、掛上 /api
  → app/routers/notes.py     網址、HTTP 方法、404／201／204
  → app/schemas/notes.py     檢查進來的 JSON、限制出去的欄位
  → app/repositories/notes.py  寫 SQL
  → app/core/db.py           用 .env 的 DATABASE_URL 連 PostgreSQL
```

Router 不寫 SQL。Schema 不連資料庫。Repository 不決定 HTTP 狀態碼。

## 檔案各自做什麼

| 路徑 | 做什麼 |
|---|---|
| `run.bat` | 用 venv 的 Python 啟動 uvicorn，聽 `0.0.0.0:7777` |
| `.env` | 本機連線字串，不進 Git |
| `app/main.py` | 建立 app；註冊 `/api/health`、`/api/version`、`POST /api/items`；掛 notes 路由；回前端 `webui-lab` 的 html／css；自訂 `/api/docs` |
| `app/routers/notes.py` | notes 的 REST 端點，以及舊的 `GET /api/note/{id}` |
| `app/schemas/notes.py` | `NoteCreate`：新增／更新要送的 body。`NoteResponse`：回給前端的一筆 note |
| `app/repositories/notes.py` | `notes` 表的查詢、新增、更新、刪除 |
| `app/core/db.py` | `get_connection()`，讀 `DATABASE_URL` |
| `app/core/db_test.py` | 只測連線，不走 API |
| `psql/notes.sql` | 建 `notes` 表與練習資料，在 psql 執行，不是程式執行 |
| `psql/createdb.sql` | 建資料庫與開發帳號，同樣只給 psql 用 |

靜態頁限制（只出 `.html`／`.css`）目前仍寫在 `main.py` 的 `HtmlCssOnlyStaticFiles`，還沒拆到 `app/core/static_files.py`。

## 端點對到哪個函式

`main.py` 用 `include_router(..., prefix="/api")`，所以 router 裡寫 `/notes`，對外是 `/api/notes`。

| HTTP | 對外路徑 | 函式 | 狀態 |
|---|---|---|---|
| POST | `/api/notes` | `create_note` | 201 |
| GET | `/api/notes` | `list_notes` | 200 |
| GET | `/api/notes/{id}` | `get_note` | 200 或 404 |
| PUT | `/api/notes/{id}` | `update_note` | 200 或 404 |
| DELETE | `/api/notes/{id}` | `delete_note` | 204 或 404 |
| GET | `/api/note/{id}` | `get_note_legacy` | 舊路徑，內部仍呼叫同一個 repository |

找不到資料時，404 是在 router 用 `HTTPException` 回的，repository 只回 `None`。

## 還沒做的（文件後半的 ORM 範例）

`psql.md` 後半示範 SQLAlchemy（`app/models`、`Session`、`db.add()`）。現在沒有那一層，SQL 直接寫在 repository，由 `psycopg` 送出。
