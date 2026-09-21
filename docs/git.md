## Conventional Commits
```powershell
git commit -m "feat: add project landing page"
git commit -m "style: add responsive navigation"
git commit -m "feat: add form validation"
git commit -m "fix: handle failed API request"
git commit -m "security: sanitize user generated content"
git commit -m "docs: add week 8 learning notes"
```

## 何時使用

| Commit | 使用時機 |
|---|---|
| `feat:` | 新增使用者可使用的功能 |
| `fix:` | 修正錯誤或異常行為 |
| `style:` | 只改外觀、CSS、排版，不改功能 |
| `security:` | 安全性修正，例如 XSS、權限、輸入消毒 |
| `docs:` | 只修改文件、README、學習筆記 |
| `refactor:` | 重構程式，但功能和行為不變 |
| `test:` | 新增或修改測試 |
| `chore:` | 依賴、設定、建置、工具等維護工作 |
| `perf:` | 效能改善 |

| 類型 | 用途 | 範例 |
|---|---|---|
| `refactor:` | 重整程式結構，但不改變使用者看到的功能 | `refactor: split API routes into modules` |
| `test:` | 新增或修改自動化測試 | `test: add health endpoint test` |
| `chore:` | 一般維護，不是功能或錯誤修正 | `chore: update Python dependencies` |
| `perf:` | 改善效能，但功能不變 | `perf: reduce database query count` |
| `build:` | 修改建置、打包或依賴建構設定 | `build: update Python build configuration` |
| `ci:` | 修改 CI/CD 自動化流程 | `ci: add GitHub Actions workflow` |
```text
feat: 新功能
fix: 修錯誤
docs: 文件
test: 測試
chore: 依賴與一般維護
refactor: 重整程式
```