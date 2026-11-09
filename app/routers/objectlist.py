from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import get_current_member
from app.repositories import objectlist as objectlist_repo
from app.schemas.objectlist import ObjectDetail, ObjectListPage

router = APIRouter(tags=["objectlist"], dependencies=[Depends(get_current_member)])


@router.get("/objectlist/cid/{cid}", response_model=ObjectListPage)
def get_objectlist(
    cid: int,
    q: str | None = Query(None, description="關鍵字（title/des ILIKE）"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
) -> dict:
    """W09：reuse vd_objectlist；動態 q／page／size 在 FastAPI 參數化查詢。"""
    return objectlist_repo.list_by_cid_page(cid, q=q, page=page, size=size)


@router.get("/object/oid/{oid}", response_model=ObjectDetail)
def get_object(oid: int) -> dict:
    """講義：vd_object 取得物件詳情"""
    row = objectlist_repo.get_by_oid(oid)
    if not row:
        raise HTTPException(status_code=404, detail="找不到這個物件")
    return row
