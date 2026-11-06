from pydantic import BaseModel, ConfigDict, Field


class ObjectListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cid: int
    oid: int
    title: str | None = None
    class_: str | None = Field(default=None, alias="class")
    des: str | None = None
    rank: int | None = None
    mg: int | None = None
    video_path: str | None = None
    picture: str | None = None


class ObjectDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    oid: int
    title: str | None = None
    class_: str | None = Field(default=None, alias="class")
    des: str | None = None
    address: str | None = None
    telephone: str | None = None
    sourceurl: str | None = None
    nclick: int = 0
    ename: str | None = None
    purpose: str | None = None
    steps: list[str] = []
    sets: int | None = None
    reps: int | None = None
    hold_seconds: int | None = None
    frequency: str | None = None
    dose_note: str | None = None
    source_refs: list[str] = []
    video_path: str | None = None
    reviewed: int | None = None
    picture: str | None = None
