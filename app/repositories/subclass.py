from app.core.db import get_connection


def list_subclass(pcid: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT pcid, parent_name, cid, child_name
                FROM vd_subclass
                WHERE pcid = %s
                ORDER BY cid
                """,
                (pcid,),
            )
            return [
                {
                    "pcid": row[0],
                    "parent_name": row[1],
                    "cid": row[2],
                    "child_name": row[3],
                }
                for row in cur.fetchall()
            ]
