-- 運動教學 I3S：在「首頁」下另開「運動分類」（不掛在 hahahan 下）
-- 用法：psql -h 127.0.0.1 -p 5433 -U hahahan -d fastapi_dev -f 01_exercise_catalog.sql

-- 教學物件延伸表（object 本體 + 多目錄 CO）
CREATE TABLE IF NOT EXISTS exercise (
  oid           integer PRIMARY KEY REFERENCES object(oid) ON DELETE CASCADE,
  ename         text,
  purpose       text,
  steps         jsonb NOT NULL DEFAULT '[]'::jsonb,
  sets          integer,
  reps          integer,
  hold_seconds  integer,
  frequency     text,
  dose_note     text,
  source_refs   jsonb NOT NULL DEFAULT '[]'::jsonb,
  video_path    text,
  reviewed      smallint NOT NULL DEFAULT 0,
  picture       text
);

-- 根：首頁 → 運動分類
SELECT insertClass(0, '首頁', '運動分類');
UPDATE class SET code = 'exercise_catalog' WHERE name = '運動分類' AND idpath = '0/' || cid::text;

-- 四大群組
SELECT insertClass(
  (SELECT cid FROM class WHERE code = 'exercise_catalog'),
  '運動分類',
  '訓練目標'
);
UPDATE class SET code = 'goal'
WHERE name = '訓練目標'
  AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'exercise_catalog');

SELECT insertClass(
  (SELECT cid FROM class WHERE code = 'exercise_catalog'),
  '運動分類',
  '姿勢'
);
UPDATE class SET code = 'position'
WHERE name = '姿勢'
  AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'exercise_catalog');

SELECT insertClass(
  (SELECT cid FROM class WHERE code = 'exercise_catalog'),
  '運動分類',
  '器材'
);
UPDATE class SET code = 'equipment'
WHERE name = '器材'
  AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'exercise_catalog');

SELECT insertClass(
  (SELECT cid FROM class WHERE code = 'exercise_catalog'),
  '運動分類',
  '難度'
);
UPDATE class SET code = 'level'
WHERE name = '難度'
  AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'exercise_catalog');

-- 訓練目標 leaves
SELECT insertClass((SELECT cid FROM class WHERE code = 'goal'), '訓練目標', '足內在肌訓練');
UPDATE class SET code = 'intrinsic' WHERE name = '足內在肌訓練' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'goal');

SELECT insertClass((SELECT cid FROM class WHERE code = 'goal'), '訓練目標', '小腿與後脛肌強化');
UPDATE class SET code = 'calf_tibpost' WHERE name = '小腿與後脛肌強化' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'goal');

SELECT insertClass((SELECT cid FROM class WHERE code = 'goal'), '訓練目標', '髖部穩定');
UPDATE class SET code = 'hip' WHERE name = '髖部穩定' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'goal');

SELECT insertClass((SELECT cid FROM class WHERE code = 'goal'), '訓練目標', '平衡與控制');
UPDATE class SET code = 'balance' WHERE name = '平衡與控制' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'goal');

SELECT insertClass((SELECT cid FROM class WHERE code = 'goal'), '訓練目標', '伸展放鬆');
UPDATE class SET code = 'stretch' WHERE name = '伸展放鬆' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'goal');

-- 姿勢 leaves
SELECT insertClass((SELECT cid FROM class WHERE code = 'position'), '姿勢', '坐姿');
UPDATE class SET code = 'seated' WHERE name = '坐姿' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'position');

SELECT insertClass((SELECT cid FROM class WHERE code = 'position'), '姿勢', '站姿');
UPDATE class SET code = 'standing' WHERE name = '站姿' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'position');

SELECT insertClass((SELECT cid FROM class WHERE code = 'position'), '姿勢', '側躺');
UPDATE class SET code = 'sidelying' WHERE name = '側躺' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'position');

-- 器材 leaves
SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '徒手（可扶牆）');
UPDATE class SET code = 'none' WHERE name = '徒手（可扶牆）' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '毛巾');
UPDATE class SET code = 'towel' WHERE name = '毛巾' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '彈力帶');
UPDATE class SET code = 'band' WHERE name = '彈力帶' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '彈珠與小碗');
UPDATE class SET code = 'marble' WHERE name = '彈珠與小碗' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '階梯');
UPDATE class SET code = 'stairs' WHERE name = '階梯' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

SELECT insertClass((SELECT cid FROM class WHERE code = 'equipment'), '器材', '按摩球');
UPDATE class SET code = 'ball' WHERE name = '按摩球' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'equipment');

-- 難度 leaves
SELECT insertClass((SELECT cid FROM class WHERE code = 'level'), '難度', '入門');
UPDATE class SET code = 'beginner' WHERE name = '入門' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'level');

SELECT insertClass((SELECT cid FROM class WHERE code = 'level'), '難度', '中階');
UPDATE class SET code = 'intermediate' WHERE name = '中階' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'level');

SELECT insertClass((SELECT cid FROM class WHERE code = 'level'), '難度', '進階');
UPDATE class SET code = 'advanced' WHERE name = '進階' AND idpath LIKE (SELECT idpath || '/%' FROM class WHERE code = 'level');

-- 確認
SELECT cid, name, code, idpath, namepath
FROM class
WHERE idpath LIKE (SELECT idpath || '%' FROM class WHERE code = 'exercise_catalog')
   OR code = 'exercise_catalog'
ORDER BY idpath;
