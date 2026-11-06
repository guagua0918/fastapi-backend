from __future__ import annotations

import json

from app.core.db import get_connection


def list_by_cid(cid: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT cid, oid, title, class, des, rank, mg, video_path, picture
                FROM vd_objectlist
                WHERE cid = %s
                ORDER BY rank, oid
                """,
                (cid,),
            )
            return [
                {
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
                for r in cur.fetchall()
            ]


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
