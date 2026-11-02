import math
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from psycopg.errors import UniqueViolation

from app.core.csi_constants import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    CORRECTION_PIXEL_EPS,
    FLAT_THRESHOLD,
    LETTERBOX_FILL,
)
from app.core.security import get_current_member
from app.core.storage import footprint_dir, relative_to_data, resolve_data_path
from app.repositories import scan as scan_repo
from app.schemas.scan import FootprintConfirm, FootprintOut, PointPair, ScanSessionOut

router = APIRouter(prefix="/scan", tags=["scan"], dependencies=[Depends(get_current_member)])

_STATUS_MESSAGES = {
    "pending": "已收到照片，準備分析…",
    "sam_done": "正在校正拍攝角度…",
    "pca_done": "正在整理量測區域…",
    "toe_cropped": "正在定位關鍵量測點…",
    "cv_keypoints_done": "自動定位完成，請確認或修改。",
    "cv_failed": "自動定位不穩定，請按「修改」自行標記。",
    "user_confirmed": "已確認並存檔。",
}


def _points_from_prefix(row: dict, prefix: str) -> PointPair | None:
    keys = [f"{prefix}_{p}_{a}" for p in "abcd" for a in ("x", "y")]
    if any(row.get(k) is None for k in keys):
        return None
    return PointPair(
        a_x=row[f"{prefix}_a_x"], a_y=row[f"{prefix}_a_y"],
        b_x=row[f"{prefix}_b_x"], b_y=row[f"{prefix}_b_y"],
        c_x=row[f"{prefix}_c_x"], c_y=row[f"{prefix}_c_y"],
        d_x=row[f"{prefix}_d_x"], d_y=row[f"{prefix}_d_y"],
    )


def _preview_url(row: dict) -> str | None:
    rel = row.get("aligned_preview_path") or row.get("input_image_path")
    if not rel:
        return None
    return f"api/scan/footprints/{row['fid']}/preview"


def _to_out(row: dict) -> FootprintOut:
    status_key = row["processing_status"]
    msg = _STATUS_MESSAGES.get(status_key, "")
    if status_key == "pending" and row.get("processing_error_log") == "in_flight":
        msg = "正在分離足印輪廓…"
    return FootprintOut(
        fid=row["fid"],
        session_id=row["session_id"],
        foot_side=row["foot_side"],
        processing_status=row["processing_status"],
        processing_error_log=row["processing_error_log"]
        if row["processing_error_log"] not in (None, "in_flight")
        else None,
        is_cv_available=bool(row["is_cv_available"]),
        canvas_width=row["canvas_width"],
        canvas_height=row["canvas_height"],
        preview_url=_preview_url(row),
        cv=_points_from_prefix(row, "cv"),
        user=_points_from_prefix(row, "user"),
        forefoot_width=row["forefoot_width"],
        arch_width=row["arch_width"],
        csi_value=row["csi_value"],
        is_flat=row["is_flat"],
        status_message=msg,
    )


def _dist(ax: float, ay: float, bx: float, by: float, w: int, h: int) -> float:
    return math.hypot((ax - bx) * w, (ay - by) * h)


def _metrics_from_points(points: PointPair, width: int, height: int) -> dict:
    fore = _dist(points.a_x, points.a_y, points.b_x, points.b_y, width, height)
    arch = _dist(points.c_x, points.c_y, points.d_x, points.d_y, width, height)
    if fore < 1:
        raise HTTPException(status_code=400, detail="Forefoot points too close")
    csi = (arch / fore) * 100.0
    return {
        "forefoot_width": fore,
        "arch_width": arch,
        "csi_value": csi,
        "is_flat": csi > FLAT_THRESHOLD,
    }


def _mean_correction(cv: PointPair, user: PointPair, w: int, h: int) -> float:
    pairs = [
        (cv.a_x, cv.a_y, user.a_x, user.a_y),
        (cv.b_x, cv.b_y, user.b_x, user.b_y),
        (cv.c_x, cv.c_y, user.c_x, user.c_y),
        (cv.d_x, cv.d_y, user.d_x, user.d_y),
    ]
    total = sum(math.hypot((a - c) * w, (b - d) * h) for a, b, c, d in pairs)
    return total / 4.0


@router.post("/sessions", response_model=ScanSessionOut, status_code=status.HTTP_201_CREATED)
def create_session(member: dict = Depends(get_current_member)) -> dict:
    return scan_repo.create_session(member["id"])


@router.post("/sessions/{session_id}/complete", response_model=ScanSessionOut)
def complete_session(session_id: int, member: dict = Depends(get_current_member)) -> dict:
    row = scan_repo.complete_session(session_id, member["id"])
    if row is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return row


@router.post(
    "/sessions/{session_id}/feet/{foot_side}",
    response_model=FootprintOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_foot(
    session_id: int,
    foot_side: str,
    file: UploadFile = File(...),
    member: dict = Depends(get_current_member),
) -> FootprintOut:
    if foot_side not in ("left", "right"):
        raise HTTPException(status_code=400, detail="foot_side must be left or right")
    session = scan_repo.get_session(session_id, member["id"])
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Session is not in progress")

    title = "左足印" if foot_side == "left" else "右足印"
    try:
        row = scan_repo.create_footprint(
            mid=member["id"],
            session_id=session_id,
            foot_side=foot_side,
            title=title,
        )
    except UniqueViolation as exc:
        raise HTTPException(
            status_code=409,
            detail="This foot already exists in the session",
        ) from exc

    dest_dir = footprint_dir(member["id"], session_id, row["fid"])
    dest = dest_dir / "input.png"
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    dest.write_bytes(content)
    rel = relative_to_data(dest)
    updated = scan_repo.set_input_image(
        row["fid"],
        relative_path=rel,
        canvas_width=CANVAS_WIDTH,
        canvas_height=CANVAS_HEIGHT,
        letterbox_fill=LETTERBOX_FILL,
    )
    return _to_out(updated)


@router.get("/footprints/{fid}", response_model=FootprintOut)
def read_footprint(fid: int, member: dict = Depends(get_current_member)) -> FootprintOut:
    row = scan_repo.get_footprint(fid, member["id"])
    if row is None:
        raise HTTPException(status_code=404, detail="Footprint not found")
    return _to_out(row)


@router.get("/footprints/{fid}/preview")
def preview_file(fid: int, member: dict = Depends(get_current_member)):
    row = scan_repo.get_footprint(fid, member["id"])
    if row is None:
        raise HTTPException(status_code=404, detail="Footprint not found")
    rel = row.get("aligned_preview_path") or row.get("input_image_path")
    if not rel:
        raise HTTPException(status_code=404, detail="Preview not ready")
    try:
        path = resolve_data_path(rel)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid path") from exc
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path)


@router.post("/footprints/{fid}/confirm", response_model=FootprintOut)
def confirm_footprint(
    fid: int,
    body: FootprintConfirm,
    member: dict = Depends(get_current_member),
) -> FootprintOut:
    row = scan_repo.get_footprint(fid, member["id"])
    if row is None:
        raise HTTPException(status_code=404, detail="Footprint not found")
    if row["processing_status"] == "user_confirmed":
        return _to_out(row)

    if body.points is not None:
        points = body.points
    else:
        points = _points_from_prefix(row, "cv")
        if points is None:
            raise HTTPException(
                status_code=400,
                detail="No CV points; send points after manual marking",
            )

    w, h = row["canvas_width"], row["canvas_height"]
    metrics = _metrics_from_points(points, w, h)
    cv = _points_from_prefix(row, "cv")
    correction = None
    is_corrected = True
    if cv is not None:
        correction = _mean_correction(cv, points, w, h)
        is_corrected = correction >= CORRECTION_PIXEL_EPS

    updated = scan_repo.confirm_footprint(
        fid,
        member["id"],
        points=points.model_dump(),
        is_corrected=is_corrected,
        correction_distance=correction,
        **metrics,
    )
    return _to_out(updated)
