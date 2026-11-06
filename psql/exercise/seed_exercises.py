"""將 exercise_seed.json 寫入 object + exercise + co（多目錄掛載）。

前置：已執行 01_exercise_catalog.sql
用法（在 fastapi-backend 根目錄）：
  .venv\\Scripts\\python.exe psql\\exercise\\seed_exercises.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL missing", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    categories = json.loads((SEED_DIR / "category_seed.json").read_text(encoding="utf-8"))
    exercises = json.loads((SEED_DIR / "exercise_seed.json").read_text(encoding="utf-8"))

    # category_seed.json 是扁平葉目錄列表：[{group, code, CName, ...}, ...]
    leaf_codes: set[str] = {item["code"] for item in categories}

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT cid FROM class WHERE code = %s",
                ("exercise_catalog",),
            )
            row = cur.fetchone()
            if not row:
                raise SystemExit("找不到 code=exercise_catalog，請先跑 01_exercise_catalog.sql")
            catalog_cid = row[0]

            cur.execute(
                "SELECT code, cid FROM class WHERE code = ANY(%s)",
                (list(leaf_codes),),
            )
            code_to_cid = {code: cid for code, cid in cur.fetchall()}
            missing = leaf_codes - set(code_to_cid)
            if missing:
                raise SystemExit(f"目錄 code 尚未建好：{sorted(missing)}")

            # 可重跑：清掉既有 exercise 物件（及其 co / exercise 列）
            cur.execute(
                """
                SELECT o.oid
                FROM object o
                WHERE o.class = 'exercise'
                """
            )
            old_oids = [r[0] for r in cur.fetchall()]
            if old_oids:
                cur.execute("DELETE FROM co WHERE oid = ANY(%s)", (old_oids,))
                cur.execute("DELETE FROM exercise WHERE oid = ANY(%s)", (old_oids,))
                cur.execute("DELETE FROM object WHERE oid = ANY(%s)", (old_oids,))

            inserted = 0
            for ex in exercises:
                title = ex["CName"]
                purpose = (ex.get("purpose") or "")[:1000]
                cur.execute(
                    """
                    INSERT INTO object (title, class, des, nclick)
                    VALUES (%s, 'exercise', %s, 0)
                    RETURNING oid
                    """,
                    (title, purpose),
                )
                oid = cur.fetchone()[0]

                dose = ex.get("dose") or {}
                cur.execute(
                    """
                    INSERT INTO exercise (
                      oid, ename, purpose, steps,
                      sets, reps, hold_seconds, frequency, dose_note,
                      source_refs, video_path, reviewed, picture
                    ) VALUES (
                      %s, %s, %s, %s::jsonb,
                      %s, %s, %s, %s, %s,
                      %s::jsonb, %s, %s, %s
                    )
                    """,
                    (
                        oid,
                        ex.get("EName"),
                        ex.get("purpose"),
                        json.dumps(ex.get("steps") or [], ensure_ascii=False),
                        dose.get("sets", ex.get("sets")),
                        dose.get("reps", ex.get("reps")),
                        dose.get("hold_seconds", ex.get("hold_seconds")),
                        dose.get("frequency", ex.get("frequency")),
                        dose.get("note", ex.get("dose_note")),
                        json.dumps(ex.get("source_refs") or [], ensure_ascii=False),
                        ex.get("video_path"),
                        1 if ex.get("reviewed") else 0,
                        ex.get("picture"),
                    ),
                )

                for i, code in enumerate(ex.get("categories") or []):
                    cid = code_to_cid[code]
                    cur.execute(
                        """
                        INSERT INTO co (cid, oid, rank, mg)
                        VALUES (%s, %s, %s, 0)
                        ON CONFLICT DO NOTHING
                        """,
                        (cid, oid, i),
                    )

                # 也掛在「運動分類」根，方便一覽全部教學物件
                cur.execute(
                    """
                    INSERT INTO co (cid, oid, rank, mg)
                    VALUES (%s, %s, %s, 0)
                    ON CONFLICT DO NOTHING
                    """,
                    (catalog_cid, oid, 100 + inserted),
                )
                inserted += 1

            # 更新各目錄 nobject
            cur.execute(
                """
                UPDATE class c
                SET nobject = (
                  SELECT COUNT(*) FROM co WHERE cid = c.cid
                )
                WHERE c.code = 'exercise_catalog'
                   OR c.idpath LIKE (
                     SELECT idpath || '/%' FROM class WHERE code = 'exercise_catalog'
                   )
                """
            )

        conn.commit()
        print(f"seeded {inserted} exercises under 運動分類 (cid={catalog_cid})")
        print(f"leaf codes mapped: {len(code_to_cid)}")


if __name__ == "__main__":
    main()
