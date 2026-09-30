from app.core.db import get_connection

_COLUMNS = "id, title, content, created_at"


def _to_dict(row) -> dict:
    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "created_at": row[3].isoformat(),
    }


def list_notes() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {_COLUMNS} FROM notes ORDER BY id")
            return [_to_dict(row) for row in cur.fetchall()]


def get_note(note_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT {_COLUMNS} FROM notes WHERE id = %s",
                (note_id,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return _to_dict(row)


def create_note(title: str, content: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO notes (title, content)
                VALUES (%s, %s)
                RETURNING {_COLUMNS}
                """,
                (title, content),
            )
            row = cur.fetchone()
    return _to_dict(row)


def update_note(note_id: int, title: str, content: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE notes
                SET title = %s, content = %s
                WHERE id = %s
                RETURNING {_COLUMNS}
                """,
                (title, content, note_id),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return _to_dict(row)


def delete_note(note_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
            row = cur.fetchone()
    return row is not None
