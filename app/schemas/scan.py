from pydantic import BaseModel, Field


class ScanSessionOut(BaseModel):
    id: int
    status: str


class PointPair(BaseModel):
    a_x: float
    a_y: float
    b_x: float
    b_y: float
    c_x: float
    c_y: float
    d_x: float
    d_y: float


class FootprintConfirm(BaseModel):
    """空 body = 採用目前 CV 建議點；有四點 = 使用者修改後的座標（0~1）。"""
    points: PointPair | None = None


class FootprintOut(BaseModel):
    fid: int
    session_id: int
    foot_side: str
    processing_status: str
    processing_error_log: str | None = None
    is_cv_available: bool
    canvas_width: int
    canvas_height: int
    preview_url: str | None = None
    cv: PointPair | None = None
    user: PointPair | None = None
    forefoot_width: float | None = None
    arch_width: float | None = None
    csi_value: float | None = None
    is_flat: bool | None = None
    status_message: str = Field(default="")
