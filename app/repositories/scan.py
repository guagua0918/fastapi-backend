from app.core.csi_constants import SCAN_CLASS_CID
from app.core.db import get_connection

_FOOTPRINT_COLS = """
    fid, session_id, mid, foot_side, created_at,
    input_image_path, canvas_width, canvas_height, letterbox_fill,
    sam_mask_path, pca_angle_deg, pca_aligned_mask_path, toe_cropped_mask_path,
    aligned_preview_path, processing_status, processing_error_log,
    cv_a_x, cv_a_y, cv_b_x, cv_b_y, cv_c_x, cv_c_y, cv_d_x, cv_d_y,
    user_a_x, user_a_y, user_b_x, user_b_y, user_c_x, user_c_y, user_d_x, user_d_y,
    is_cv_available, correction_distance, is_corrected,
    forefoot_width, arch_width, csi_value, is_flat
"""


def _row_to_footprint(row) -> dict:
    keys = [
        "fid", "session_id", "mid", "foot_side", "created_at",
        "input_image_path", "canvas_width", "canvas_height", "letterbox_fill",
        "sam_mask_path", "pca_angle_deg", "pca_aligned_mask_path", "toe_cropped_mask_path",
        "aligned_preview_path", "processing_status", "processing_error_log",
        "cv_a_x", "cv_a_y", "cv_b_x", "cv_b_y", "cv_c_x", "cv_c_y", "cv_d_x", "cv_d_y",
        "user_a_x", "user_a_y", "user_b_x", "user_b_y", "user_c_x", "user_c_y", "user_d_x", "user_d_y",
        "is_cv_available", "correction_distance", "is_corrected",
        "forefoot_width", "arch_width", "csi_value", "is_flat",
    ]
    return dict(zip(keys, row))


def create_session(mid: int) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO scan_session (mid)
                VALUES (%s)
                RETURNING id, status
                """,
                (mid,),
            )
            row = cur.fetchone()
        conn.commit()
    return {"id": row[0], "status": row[1]}


def get_session(session_id: int, mid: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, status
                FROM scan_session
                WHERE id = %s AND mid = %s
                """,
                (session_id, mid),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return {"id": row[0], "status": row[1]}


def complete_session(session_id: int, mid: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE scan_session
                SET status = 'completed'
                WHERE id = %s AND mid = %s
                RETURNING id, status
                """,
                (session_id, mid),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        return None
    return {"id": row[0], "status": row[1]}


def create_footprint(
    *,
    mid: int,
    session_id: int,
    foot_side: str,
    title: str,
) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO object (title, class, nclick)
                VALUES (%s, %s, 0)
                RETURNING oid
                """,
                (title, "footprint"),
            )
            oid = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO co (cid, oid, rank, mg)
                VALUES (%s, %s, 0, 0)
                ON CONFLICT DO NOTHING
                """,
                (SCAN_CLASS_CID, oid),
            )
            cur.execute(
                f"""
                INSERT INTO footprint (fid, session_id, mid, foot_side)
                VALUES (%s, %s, %s, %s)
                RETURNING {_FOOTPRINT_COLS}
                """,
                (oid, session_id, mid, foot_side),
            )
            row = cur.fetchone()
        conn.commit()
    return _row_to_footprint(row)


def get_footprint(fid: int, mid: int | None = None) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if mid is None:
                cur.execute(
                    f"SELECT {_FOOTPRINT_COLS} FROM footprint WHERE fid = %s",
                    (fid,),
                )
            else:
                cur.execute(
                    f"""
                    SELECT {_FOOTPRINT_COLS}
                    FROM footprint
                    WHERE fid = %s AND mid = %s
                    """,
                    (fid, mid),
                )
            row = cur.fetchone()
    if row is None:
        return None
    return _row_to_footprint(row)


def set_input_image(
    fid: int,
    *,
    relative_path: str,
    canvas_width: int,
    canvas_height: int,
    letterbox_fill: str,
) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE footprint
                SET input_image_path = %s,
                    canvas_width = %s,
                    canvas_height = %s,
                    letterbox_fill = %s,
                    processing_status = 'pending',
                    processing_error_log = NULL,
                    is_cv_available = false
                WHERE fid = %s
                RETURNING {_FOOTPRINT_COLS}
                """,
                (relative_path, canvas_width, canvas_height, letterbox_fill, fid),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        return None
    return _row_to_footprint(row)


def confirm_footprint(
    fid: int,
    mid: int,
    *,
    points: dict,
    forefoot_width: float,
    arch_width: float,
    csi_value: float,
    is_flat: bool,
    is_corrected: bool,
    correction_distance: float | None,
) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE footprint
                SET user_a_x = %s, user_a_y = %s,
                    user_b_x = %s, user_b_y = %s,
                    user_c_x = %s, user_c_y = %s,
                    user_d_x = %s, user_d_y = %s,
                    forefoot_width = %s,
                    arch_width = %s,
                    csi_value = %s,
                    is_flat = %s,
                    is_corrected = %s,
                    correction_distance = %s,
                    processing_status = 'user_confirmed'
                WHERE fid = %s AND mid = %s
                RETURNING {_FOOTPRINT_COLS}
                """,
                (
                    points["a_x"], points["a_y"],
                    points["b_x"], points["b_y"],
                    points["c_x"], points["c_y"],
                    points["d_x"], points["d_y"],
                    forefoot_width, arch_width, csi_value, is_flat,
                    is_corrected, correction_distance,
                    fid, mid,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        return None
    return _row_to_footprint(row)


def claim_pending_job() -> dict | None:
    """Worker 用：取出一筆 pending。"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {_FOOTPRINT_COLS}
                FROM footprint
                WHERE processing_status = 'pending'
                  AND input_image_path IS NOT NULL
                ORDER BY created_at
                FOR UPDATE SKIP LOCKED
                LIMIT 1
                """
            )
            row = cur.fetchone()
            if row is None:
                conn.commit()
                return None
            cur.execute(
                """
                UPDATE footprint
                SET processing_error_log = 'in_flight'
                WHERE fid = %s AND processing_status = 'pending'
                """,
                (row[0],),
            )
        conn.commit()
    return _row_to_footprint(row)


def update_cv_progress(fid: int, status: str, **fields) -> None:
    allowed = {
        "sam_mask_path", "pca_angle_deg", "pca_aligned_mask_path",
        "toe_cropped_mask_path", "aligned_preview_path",
        "processing_error_log",
        "cv_a_x", "cv_a_y", "cv_b_x", "cv_b_y",
        "cv_c_x", "cv_c_y", "cv_d_x", "cv_d_y",
        "is_cv_available", "forefoot_width", "arch_width", "csi_value", "is_flat",
        "canvas_width", "canvas_height",
    }
    sets = ["processing_status = %s"]
    values: list = [status]
    for key, value in fields.items():
        if key not in allowed:
            raise ValueError(f"disallowed field: {key}")
        sets.append(f"{key} = %s")
        values.append(value)
    values.append(fid)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE footprint SET {', '.join(sets)} WHERE fid = %s",
                values,
            )
        conn.commit()
