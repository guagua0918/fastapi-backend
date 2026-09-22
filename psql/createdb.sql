-- W02: 建立開發用資料庫與使用者（用 postgres 超級使用者執行）
-- 若帳號/資料庫已存在，對應語句可略過或會報錯，屬正常。

CREATE USER dev_user WITH PASSWORD 'your_password';
CREATE DATABASE fastapi_dev OWNER dev_user;

\connect fastapi_dev
GRANT USAGE, CREATE ON SCHEMA public TO dev_user;
