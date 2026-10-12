from fastapi import APIRouter

from app.repositories import subclass as subclass_repo
from app.schemas.subclass import SubclassItem

router = APIRouter(tags=["subclass"])


@router.get("/subclass/pcid/{pcid}", response_model=list[SubclassItem])
def get_subclass(pcid: int) -> list[dict]:
    return subclass_repo.list_subclass(pcid)
