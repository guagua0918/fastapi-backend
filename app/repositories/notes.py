"""Notes repository：W08 改為 async + AsyncConnectionPool。"""
from app.core.db import get_async_connection

_COLUMNS = "id, title, content, created_at"


def _to_dict(row) -> dict:
    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "created_at": row[3].isoformat(),
    }


async def list_notes() -> list[dict]:
    async with get_async_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT {_COLUMNS} FROM notes ORDER BY id")
            rows = await cur.fetchall()
    return [_to_dict(row) for row in rows]


async def get_note(note_id: int) -> dict | None:
    async with get_async_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT {_COLUMNS} FROM notes WHERE id = %s",
                (note_id,),
            )
            row = await cur.fetchone()
    if row is None:
        return None
    return _to_dict(row)


async def create_note(title: str, content: str) -> dict:
    async with get_async_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                INSERT INTO notes (title, content)
                VALUES (%s, %s)
                RETURNING {_COLUMNS}
                """,
                (title, content),
            )
            row = await cur.fetchone()
        await conn.commit()
    return _to_dict(row)


async def update_note(note_id: int, title: str, content: str) -> dict | None:
    async with get_async_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                UPDATE notes
                SET title = %s, content = %s
                WHERE id = %s
                RETURNING {_COLUMNS}
                """,
                (title, content, note_id),
            )
            row = await cur.fetchone()
        await conn.commit()
    if row is None:
        return None
    return _to_dict(row)


async def delete_note(note_id: int) -> bool:
    async with get_async_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
            row = await cur.fetchone()
        await conn.commit()
    return row is not None
