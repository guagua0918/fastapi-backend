-- W02 practice: notes table + 3 sample rows

CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

TRUNCATE notes RESTART IDENTITY;

INSERT INTO notes (title, content) VALUES
    ('第一則筆記', '這是 W02 練習的第一筆資料'),
    ('第二則筆記', '用 psql INSERT 進去的內容'),
    ('第三則筆記', '之後用 GET /api/note/{id} 讀取');
