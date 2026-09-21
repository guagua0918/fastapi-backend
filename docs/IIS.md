第一個概念：**服務必須綁定到可被其他電腦連線的 IP 位址**。

## 概念一：不能只綁 `127.0.0.1`

如果用：
```powershell
uvicorn app.main:app --reload
```
FastAPI 通常只監聽：
```text
127.0.0.1:8000
```


要讓同網路上的 IIS 主機能連線，服務通常要監聽：

```text
0.0.0.0
```

例如後端：

```powershell
.\venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
```

 # IIS 反向代理：FastAPI 對外公開

本機開發服務，透過學校 IIS 反向代理公開成網址。範例使用：

 ```text
 公開網址：https://demo.wke.csie.ncnu.edu.tw/s115321503/
 本機服務：http://10.22.22.170:7777/
 ```

 ## 1. 先理解整體流程

 ```text
 瀏覽器
     |
     v
 https://demo.wke.csie.ncnu.edu.tw/s115321503/
     |
     | IIS URL Rewrite + ARR
     v
 http://10.22.22.170:7777/
     |
     v
 FastAPI：前端 HTML/CSS + /api/ API
 ```

 IIS 不會替你執行 Python。它只負責接收公開網址的請求，再轉送到你的電腦。因此本機服務必須持續執行，且 IIS 主機必須能連到你的 IP 和 port。

 ## 2. 本機服務必須符合的條件

 ### 2.1 綁定 `0.0.0.0`

 `127.0.0.1` 或 `localhost` 只代表目前這台電腦。若 IIS 使用 `127.0.0.1`，它會連到 IIS 伺服器自己，而不是你的電腦。

 FastAPI 應監聽所有網路介面：

 ```powershell
 cd C:\Users\admin\code\fastapi-backend
 .\run.bat
 ```

 `run.bat` 應等同於：

 ```powershell
 venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
 ```

 確認監聽位址：

 ```powershell
 Get-NetTCPConnection -LocalPort 7777 -State Listen
 ```

 `LocalAddress` 應為 `0.0.0.0`。若是 `127.0.0.1`，其他電腦和 IIS 不能直接連線。

 ### 2.2 查詢校內 IP

 ```powershell
 ipconfig
 ```

 在目前使用的 Ethernet 或 Wi-Fi 介面找到 `IPv4 Address`。不要使用 `127.0.0.1`；`169.254.x.x` 通常代表沒有成功取得正常的網路位址。`10.x.x.x` 是私有網路位址，通常只能在校內網路或校方 VPN 中使用。

 ### 2.3 Port 只能由一個服務使用

 同一個 IP 的同一個 port 不能同時由 Node `http-server` 和 Uvicorn 使用。若看到 `WinError 10013` 或「address already in use」，先停止佔用 port 的服務，再啟動 FastAPI。

 查詢程序：

 ```powershell
 Get-NetTCPConnection -LocalPort 7777 -State Listen
 Get-Process -Id <OwningProcess>
 ```

 ## 3. FastAPI 的 Web App 和 API

 W03 的目標是由同一個 FastAPI 服務前端與 API：

 ```text
 /                 前端 index.html
 /api/health       健康檢查 API
 /api/version      版本 API
 /api/items        Item API
 ```

 前端資料夾可以是後端專案的同級資料夾：

 ```text
 code/
 ├─ webui-lab/
 │  └─ index.html
 └─ fastapi-backend/
        ├─ app/main.py
        └─ run.bat
 ```

 `main.py` 的重要概念：

 - 用 `StaticFiles` 提供前端檔案。
 - 用 `APIRouter(prefix="/api")` 統一 API 路徑。
 - 根路徑 `/` 回傳前端 `index.html`。
 - 依老師要求限制公開靜態檔案的副檔名。

 目前的 W03 限制是只允許 `.html` 和 `.css`；如果前端開始使用 JavaScript，必須依老師要求調整限制，否則 `.js` 會回傳 `404`。

 ## 4. 本機驗收順序

 保持運行，再開另一個 PowerShell。不要只測 `localhost`，要逐層確認。

 ### 4.1 本機回環測試

 ```powershell
 curl.exe -i http://127.0.0.1:7777/
 curl.exe -i http://127.0.0.1:7777/api/health
 ```

 預期首頁是 `200 OK`，API 回傳：

 ```json
 {"status":"ok"}
 ```

 ### 4.2 使用校內 IP 測試

 ```powershell
 curl.exe -i http://你的校內IP:7777/
 curl.exe -i http://你的校內IP:7777/api/health
 Test-NetConnection 你的校內IP -Port 7777
 ```

 預期 `TcpTestSucceeded : True`。若本機成功、IP 失敗，優先檢查 Windows 防火牆、網路介面和服務是否真的綁定 `0.0.0.0`。

 ### 4.3 另一台裝置測試

 請用同一個可互通校內網路的電腦或裝置開啟：

 ```text
 http://你的校內IP:7777/
 http://你的校內IP:7777/api/health
 ```

 這一步很重要：自己的電腦可以連，不代表 IIS 主機或其他裝置也可以連。手機行動網路通常不能直接連到校內的 `10.x.x.x` 位址，除非有適當 VPN 或路由。

 ## 5. IIS 設定的角色

 IIS 通常需要：

 1. URL Rewrite
 2. Application Request Routing（ARR）並啟用 Proxy

 在 IIS 站台下建立自己的虛擬目錄，例如：

 ```text
 Alias：s115321503
 ```

 Alias 不要填前面的 `/`。它決定公開 URL 的路徑，但不是本機資料夾，也不是 FastAPI port。

 Physical path 是 IIS 伺服器上的資料夾，必須由管理者提供或確認權限；它不是你自己電腦上的 `C:\Users\admin\code\fastapi-backend`。

 ### Rewrite 規則要理解的欄位

 先前的設定可以當範本，但不能直接複製。至少要替換：

 ```text
 Alias / 學號
 目標 IP
 目標 port
 ```

 例如目標應是：

 ```text
 http://10.22.22.170:7777
 ```

 `Rewrite` 是 IIS 內部轉送，瀏覽器網址仍然保持公開網址。公開請求：

 ```text
 /s115321503/api/health
 ```

 應轉成後端請求：

 ```text
 /api/health
 ```

 如果規則放在虛擬目錄內，IIS 可能已先去掉 `s115321503` 前綴；如果放在站台根目錄，匹配字串可能仍包含學號前綴。設定前要確認 `web.config` 的位置，不能只看正規表示式表面上是否相似。

 ## 6. 公開網址驗收

 假設公開網址是：

 ```text
 https://demo.wke.csie.ncnu.edu.tw/s115321503
 ```

 依序測試：

 ```powershell
 curl.exe -i https://demo.wke.csie.ncnu.edu.tw/s115321503/
 curl.exe -i https://demo.wke.csie.ncnu.edu.tw/s115321503/api/health
 curl.exe -i https://demo.wke.csie.ncnu.edu.tw/s115321503/api/version
 ```

 預期：

 - 首頁：`200 OK`，內容是自己的 `index.html`。
 - `/api/health`：`200 OK` 與 `{"status":"ok"}`。
 - `/api/version`：`200 OK` 與 `{"version":"0.1.0"}`。

 測試 `POST /api/items`：

 ```powershell
 curl.exe -i -X POST `
     -H "Content-Type: application/json" `
     -d '{"name":"Keyboard","price":99.5}' `
     https://demo.wke.csie.ncnu.edu.tw/s115321503/api/items
 ```

 正確資料應回傳 `200` 和 Item JSON。故意省略 `price` 或傳入無法轉成數字的值，應回傳 `422`；這是 Pydantic 驗證正常運作，不是 IIS 失敗。

 ### 瀏覽器快取

 修改 HTML/CSS 後，瀏覽器可能仍顯示舊檔案。排查時使用：

 1. 無痕視窗。
 2. F12 → Network。
 3. 勾選 Disable cache。
 4. 重新整理。

 先用 `curl.exe` 確認伺服器實際回應，再判斷是否只是瀏覽器快取。

 ## 7. 狀態碼與排查方向

 ```text
 200        請求成功
 404        路徑、Rewrite、靜態檔或 API 前綴不符合
 422        API 請求 body 通過到 FastAPI，但資料格式不符合模型
 500        IIS、web.config 或應用程式內部錯誤
 502        IIS 無法連到本機 IP:port，檢查服務、防火牆和網路
 Timeout    服務未啟動、IP 錯誤、port 被擋或路由不可達
 ```

 建議依這個順序縮小問題：

 ```text
 1. 本機 127.0.0.1:7777
 2. 本機校內IP:7777
 3. 另一台裝置連校內IP:7777
 4. IIS 轉送 /api/health
 5. IIS 轉送首頁
 6. 完整前端操作
 ```

 第 1 步失敗是應用程式問題；第 1 步成功、第 2 步失敗通常是綁定位址或防火牆問題；第 3 步成功、第 4 步失敗則優先查 IIS Rewrite、ARR 或伺服器到用戶端的網路路徑。

 ## 8. 同學來設定 IIS 前的交付清單

 同學至少應完成：

 - 可以執行 `venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload`，服務監聽 `0.0.0.0:7777`。
 - 首頁可以回傳自己的 HTML。
 - `/api/health` 回傳 `{"status":"ok"}`。
 - `/api/version` 回傳 `{"version":"0.1.0"}`。
 - `/api/items` 正確資料成功，錯誤資料回傳 `422`。
 - 用目前校內 IP 測試成功。
 - 另一台可互通裝置測試成功。
 - 提供學號、Alias、目前 IP、port 和本機測試結果。

 應提供給 IIS 管理者的資料格式：

 ```text
 學號：115321503
 Virtual Directory：s115321503
 目前校內 IP：10.22.22.170
 服務 Port：7777
 首頁：http://10.22.22.170:7777/
 健康檢查：http://10.22.22.170:7777/api/health
 ```

 只有在本機和其他裝置測試通過後，才適合設定 IIS。這樣公開網址失敗時，問題範圍才會集中在 IIS，而不是同時混有 Python、port、防火牆和前端路徑問題。

 ## 9. 和其他課程的關係

 W01 的 FastAPI 基礎練習包含 `/health`、`/version`、Pydantic `Item` 和 `requirements.txt`。W03 為了區分網站與 API，把路徑統一成 `/api/...`。

---

你的理解接近，但其實還有一個更大的差異：**兩份規則的匹配範圍不同**。

## 1. `web.config` 是做什麼？

`web.config` 是 IIS 的設定檔，告訴 IIS：

- 哪些網址要匹配
- 匹配後要重新導向還是反向代理
- 要送到哪個後端 IP 和 port
- 是否保留 query string
- 是否停止繼續套用其他規則

你的情境：

```text
公開網址
https://demo.wke.csie.ncnu.edu.tw/s115999999/api/docs
```

IIS 讀取 `web.config` 後，轉送為：

```text
http://10.21.26.181:7777/api/docs
```

它不負責執行 FastAPI，而是負責「網址路由與轉送」。

---

## 2. `R:1` 和 `R:3` 是什麼？

它們代表 `<match>` 正規表示式中，第幾個括號捕捉到的內容。

### 老師的規則

```xml
<match url="^s115999999/(.*)$" />
```

只有一組括號：

```text
^s115999999/(.*)$
             └─ R:1
```

請求：

```text
s115999999/api/docs
```

得到：

```text
R:1 = api/docs
```

所以：

```xml
url="http://10.21.26.181:7777/{R:1}"
```

會變成：

```text
http://10.21.26.181:7777/api/docs
```

### 你原本的規則

```xml
<match url="^((.*)/s115321503/?)?(.*)" />
```

有三組括號：

```text
^((.*)/s115321503/?)?(.*)
  │    │              │
 R:1  R:2            R:3
```

因此你使用：

```xml
{R:3}
```

是因為最後的 `(.*)` 捕捉了實際要轉送的路徑。

例如：

```text
s115321503/api/docs
```

大致會得到：

```text
R:1 = s115321503/
R:2 = ...
R:3 = api/docs
```

所以最後也是轉送到：

```text
http://10.22.22.170:7777/api/docs
```

**重點：`R:1` 或 `R:3` 沒有固定意義，完全取決於前面正規表示式的括號數量和位置。**

---

## 3. 為什麼老師改用 `R:1`？

老師的規則比較簡單：

```xml
^s115999999/(.*)$
```

它只捕捉「學號後面的所有路徑」，因此直接使用：

```xml
{R:1}
```

優點是：

- 容易閱讀
- 容易除錯
- 不需要猜三層括號
- 不容易因為修改正規表示式而讓 `{R:3}` 失效

這是一個重要的正規表示式觀念：

> 捕捉群組的編號是從左到右計算，從 `R:1` 開始。

---

## 4. `logRewrittenUrl="true"` 是什麼？

```xml
logRewrittenUrl="true"
```

表示要求 IIS 將 Rewrite 後的目標網址記錄到 IIS log，方便除錯。

例如原始請求：

```text
/s115321503/api/docs
```

Rewrite 後：

```text
http://10.22.22.170:7777/api/docs
```

啟用後，IIS log 比較容易看出實際轉送到了哪裡。

它主要是：

```text
除錯與記錄功能
```

不會改變 URL Rewrite 的邏輯，也不會讓反向代理本身生效。

---

## 5. `appendQueryString="true"` 是什麼？

```xml
appendQueryString="true"
```

表示保留原始網址後面的 query string。

例如使用者請求：

```text
/s115999999/api/items?page=2&limit=10
```

Rewrite 後會變成：

```text
http://10.21.26.181:7777/api/items?page=2&limit=10
```

如果沒有保留，後端可能只收到：

```text
/api/items
```

Query string 常見用途：

```text
?page=2
?search=book
?sort=created_at
```

對 Swagger `/api/docs` 不一定是必要的，但對一般 API 很重要，所以老師的規則較完整。

---

## 6. 兩者是否可以同時使用？

可以：

```xml
<action
    type="Rewrite"
    url="http://10.21.26.181:7777/{R:1}"
    logRewrittenUrl="true"
    appendQueryString="true" />
```

例如：

```xml
<rule name="s115999999" stopProcessing="true">
    <match url="^s115999999/(.*)$" />
    <action
        type="Rewrite"
        url="http://10.21.26.181:7777/{R:1}"
        logRewrittenUrl="true"
        appendQueryString="true" />
</rule>
```

但是否能使用，仍取決於 `web.config` 放在哪裡：

- 站台根目錄：通常匹配 `s115999999/...`
- 虛擬目錄內：通常匹配 `...`，不再包含 `s115999999`

---

## 7. `stopProcessing="true"` 又是什麼？

```xml
stopProcessing="true"
```

規則成功匹配後，IIS 不再繼續嘗試後面的規則。

這可以避免：

```text
第一條規則已經轉送
第二條規則又再次改寫
```

造成路徑錯誤或重複轉送。

---

## 8. 你應該學到的核心觀念

### `web.config` 是 IIS 的路由設定

```text
瀏覽器 URL
  ↓
IIS Rewrite
  ↓
FastAPI URL
```

### URL Rewrite 不等於 Redirect

```xml
type="Rewrite"
```

是伺服器內部轉送，瀏覽器網址通常不變。

```xml
type="Redirect"
```

是回覆瀏覽器，要求它重新發送到另一個網址，網址列會改變。

老師的第一條規則就是：

```text
/s115999999 → /s115999999/
```

用來補上結尾斜線。

### `R:n` 是正規表示式的捕捉結果

```text
R:1 = 第一組括號
R:2 = 第二組括號
R:3 = 第三組括號
```

### 反向代理要保留路徑和參數

例如：

```text
公開：/s115999999/api/docs?x=1
後端：/api/docs?x=1
```

Rewrite 規則必須：

- 去掉公開路徑前綴
- 保留真正 API 路徑
- 視需要保留 query string

## 簡單比較

| 項目 | 你原本 | 老師版本 |
|---|---|---|
| 正規表示式 | 較複雜、三組捕捉 | 簡單、一組捕捉 |
| Rewrite 結果 | 用 `{R:3}` | 用 `{R:1}` |
| 日誌 | `logRewrittenUrl=true` | 未設定 |
| Query string | 預設行為 | 明確 `appendQueryString=true` |
| 可讀性 | 較難維護 | 較容易維護 |

最後要記得：**老師版本不一定「功能比較多」，而是因為他的 `web.config` 放置位置和匹配範圍已經配合好，所以可以用更簡潔的正規表示式。**