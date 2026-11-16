-- 使用者私有菜單：掛在「首頁 → 我的菜單」下，code = user_menu_{mid}
-- 用法：可重跑；已存在則略過

SELECT insertClass(0, '首頁', '我的菜單');
UPDATE class
SET code = 'user_menus'
WHERE name = '我的菜單'
  AND idpath = '0/' || cid::text;

SELECT cid, name, code, idpath, namepath
FROM class
WHERE code = 'user_menus';
