-- 個人設定：顯示名稱（與 Google OAuth 的 name 分開）
ALTER TABLE member
  ADD COLUMN IF NOT EXISTS display_name text;
