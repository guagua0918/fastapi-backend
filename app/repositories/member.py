from app.core.db import get_connection


def _to_profile(row) -> dict:
    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "display_name": row[3],
        "picture": row[4],
    }


def upsert_google_member(
    google_sub: str,
    email: str,
    name: str | None,
    picture: str | None,
    email_verified: bool,
) -> dict:
    """只更新 Google 欄位；不碰 display_name。"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO member (google_sub, email, name, picture, email_verified)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (google_sub) DO UPDATE
                SET email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    picture = EXCLUDED.picture,
                    email_verified = EXCLUDED.email_verified,
                    updated_at = now()
                RETURNING id, email, name, display_name, picture
                """,
                (google_sub, email, name, picture, email_verified),
            )
            row = cur.fetchone()
        conn.commit()
    return _to_profile(row)


def update_display_name(member_id: int, display_name: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE member
                SET display_name = %s, updated_at = now()
                WHERE id = %s AND email_verified = true
                RETURNING id, email, name, display_name, picture
                """,
                (display_name, member_id),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        return None
    return _to_profile(row)


def get_verified_member(member_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, name, display_name, picture
                FROM member
                WHERE id = %s AND email_verified = true
                """,
                (member_id,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return _to_profile(row)
