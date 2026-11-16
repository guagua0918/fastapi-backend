"""每位使用者一個菜單 class（code=user_menu_{mid}），動作用 co 掛上去。"""

from __future__ import annotations

from app.core.db import get_connection

USER_MENUS_CODE = "user_menus"


def _menu_code(mid: int) -> str:
    return f"user_menu_{mid}"


def ensure_user_menus_root() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT cid FROM class WHERE code = %s",
                (USER_MENUS_CODE,),
            )
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "SELECT insertClass(0, %s, %s)",
                ("首頁", "我的菜單"),
            )
            cid = cur.fetchone()[0]
            cur.execute(
                """
                UPDATE class
                SET code = %s
                WHERE cid = %s
                """,
                (USER_MENUS_CODE, cid),
            )
        conn.commit()
        return cid


def get_or_create_my_menu(mid: int, label: str | None = None) -> dict:
    """回傳此使用者的菜單 class；沒有就建立。

    歸屬靠 code=user_menu_{mid}。
    class.name 必須含 mid：insertClass 遇到同名子目錄會回傳既有 cid，
    不能讓兩個使用者共用「哈哈翰的菜單」這種顯示名。
    """
    root_cid = ensure_user_menus_root()
    code = _menu_code(mid)
    # 技術唯一名（前端請用 API 的 label「我的菜單」，不要直接秀這個）
    safe = "".join(ch for ch in (label or "menu") if ch.isalnum() or ch in "._-")[:40] or "menu"
    name = f"menu_{mid}_{safe}"[:100]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT cid, name, code FROM class WHERE code = %s",
                (code,),
            )
            row = cur.fetchone()
            if row:
                return {"cid": row[0], "name": row[1], "code": row[2], "mid": mid}

            cur.execute(
                "SELECT insertClass(%s, %s, %s)",
                (root_cid, "我的菜單", name),
            )
            cid = cur.fetchone()[0]
            cur.execute(
                "UPDATE class SET code = %s WHERE cid = %s",
                (code, cid),
            )
            cur.execute(
                "SELECT cid, name, code FROM class WHERE code = %s",
                (code,),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise RuntimeError(f"failed to create menu for mid={mid}")
    return {"cid": row[0], "name": row[1], "code": row[2], "mid": mid}


def get_my_menu(mid: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT cid, name, code FROM class WHERE code = %s",
                (_menu_code(mid),),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {"cid": row[0], "name": row[1], "code": row[2], "mid": mid}


def add_to_menu(mid: int, oid: int) -> dict:
    menu = get_or_create_my_menu(mid)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM object WHERE oid = %s", (oid,))
            if not cur.fetchone():
                return {"ok": False, "reason": "object_not_found"}
            cur.execute(
                """
                INSERT INTO co (cid, oid, rank, mg)
                VALUES (%s, %s, 0, 0)
                ON CONFLICT DO NOTHING
                """,
                (menu["cid"], oid),
            )
            cur.execute(
                """
                UPDATE class
                SET nobject = (SELECT COUNT(*) FROM co WHERE cid = %s)
                WHERE cid = %s
                """,
                (menu["cid"], menu["cid"]),
            )
        conn.commit()
    return {"ok": True, "cid": menu["cid"], "oid": oid}


def remove_from_menu(mid: int, oid: int) -> dict:
    menu = get_my_menu(mid)
    if not menu:
        return {"ok": False, "reason": "menu_not_found"}
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM co WHERE cid = %s AND oid = %s",
                (menu["cid"], oid),
            )
            deleted = cur.rowcount
            cur.execute(
                """
                UPDATE class
                SET nobject = (SELECT COUNT(*) FROM co WHERE cid = %s)
                WHERE cid = %s
                """,
                (menu["cid"], menu["cid"]),
            )
        conn.commit()
    return {"ok": deleted > 0, "cid": menu["cid"], "oid": oid}
