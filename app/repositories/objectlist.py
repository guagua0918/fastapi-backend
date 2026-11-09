from __future__ import annotations

import json
import math

from app.core.db import get_connection


def _row_to_item(r: tuple) -> dict:
    return {
        "cid": r[0],
        "oid": r[1],
        "title": r[2],
        "class": r[3],
        "des": r[4],
        "rank": r[5],
        "mg": r[6],
        "video_path": r[7],
        "picture": r[8],
    }


def list_by_cid(cid: int) -> list[dict]:
    """舊介面：某目錄下全部列（不分頁）。"""
    page = list_by_cid_page(cid, q=None, page=1, size=10_000)
    return page["items"]


def list_by_cid_page(
    cid: int,
    *,
    q: str | None = None,
    page: int = 1,
    size: int = 10,
) -> dict:
    """W09：VIEW 固定形狀；動態 keyword／分頁在 repository 組參數化 SQL。"""
    page = max(1, page)
    size = max(1, min(size, 100))
    offset = (page - 1) * size

    conditions = ["cid = %s"]
    params: list = [cid]

    keyword = (q or "").strip()
    if keyword:
        conditions.append("(title ILIKE %s OR COALESCE(des, '') ILIKE %s)")
        like = f"%{keyword}%"
        params.extend([like, like])

    where_sql = " AND ".join(conditions)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) FROM vd_objectlist WHERE {where_sql}",
                params,
            )
            total = int(cur.fetchone()[0])

            cur.execute(
                f"""
                SELECT cid, oid, title, class, des, rank, mg, video_path, picture
                FROM vd_objectlist
                WHERE {where_sql}
                ORDER BY rank, oid
                LIMIT %s OFFSET %s
                """,
                params + [size, offset],
            )
            items = [_row_to_item(r) for r in cur.fetchall()]

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": math.ceil(total / size) if size else 0,
    }


def get_by_oid(oid: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT oid, title, class, des, address, telephone, sourceurl, nclick,
                       ename, purpose, steps, sets, reps, hold_seconds, frequency,
                       dose_note, source_refs, video_path, reviewed, picture
                FROM vd_object
                WHERE oid = %s
                """,
                (oid,),
            )
            row = cur.fetchone()
            if not row:
                return None

            steps = row[10]
            if isinstance(steps, str):
                steps = json.loads(steps)
            refs = row[16]
            if isinstance(refs, str):
                refs = json.loads(refs)

            return {
                "oid": row[0],
                "title": row[1],
                "class": row[2],
                "des": row[3],
                "address": row[4],
                "telephone": row[5],
                "sourceurl": row[6],
                "nclick": row[7] or 0,
                "ename": row[8],
                "purpose": row[9],
                "steps": list(steps or []),
                "sets": row[11],
                "reps": row[12],
                "hold_seconds": row[13],
                "frequency": row[14],
                "dose_note": row[15],
                "source_refs": list(refs or []),
                "video_path": row[17],
                "reviewed": row[18],
                "picture": row[19],
            }
