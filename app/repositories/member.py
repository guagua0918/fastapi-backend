from app.core.db import get_connection


def upsert_google_member(
    google_sub: str,
    email: str,
    name: str | None,
    picture: str | None,
    email_verified: bool,
) -> dict:
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
                RETURNING id, email, name, picture
                """,
                (google_sub, email, name, picture, email_verified),
            )
            row = cur.fetchone()
        conn.commit()
    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "picture": row[3],
    }


def get_verified_member(member_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, name, picture
                FROM member
                WHERE id = %s AND email_verified = true
                """,
                (member_id,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "picture": row[3],
    }
