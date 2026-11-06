-- 講義作法：objectlist / object 用 VIEW，API 只 SELECT view
-- 用法：psql ... -f 02_vd_objectlist.sql

CREATE OR REPLACE VIEW vd_objectlist AS
SELECT co.cid,
       o.oid,
       o.title,
       o.class,
       o.des,
       co.rank,
       co.mg,
       e.video_path,
       e.picture
FROM co,
     object o
     LEFT JOIN exercise e ON e.oid = o.oid
WHERE co.oid = o.oid;

CREATE OR REPLACE VIEW vd_object AS
SELECT o.oid,
       o.title,
       o.class,
       o.des,
       o.address,
       o.telephone,
       o.sourceurl,
       o.nclick,
       e.ename,
       e.purpose,
       e.steps,
       e.sets,
       e.reps,
       e.hold_seconds,
       e.frequency,
       e.dose_note,
       e.source_refs,
       e.video_path,
       e.reviewed,
       e.picture
FROM object o
LEFT JOIN exercise e ON e.oid = o.oid;

-- 確認
SELECT COUNT(*) AS n FROM vd_objectlist WHERE cid = 5;
SELECT oid, title FROM vd_object WHERE class = 'exercise' LIMIT 3;
