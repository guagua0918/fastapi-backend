from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_member
from app.repositories import objectlist as objectlist_repo
from app.schemas.objectlist import ObjectDetail, ObjectListItem

router = APIRouter(tags=["objectlist"], dependencies=[Depends(get_current_member)])


@router.get("/objectlist/cid/{cid}", response_model=list[ObjectListItem])
def get_objectlist(cid: int) -> list[dict]:
    """講義：click 目錄 → SELECT * FROM vd_objectlist WHERE cid = {cid}"""
    return objectlist_repo.list_by_cid(cid)


@router.get("/object/oid/{oid}", response_model=ObjectDetail)
def get_object(oid: int) -> dict:
    """講義：vd_object 取得物件詳情"""
    row = objectlist_repo.get_by_oid(oid)
    if not row:
        raise HTTPException(status_code=404, detail="找不到這個物件")
    return row
