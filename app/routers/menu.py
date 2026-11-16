from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.exceptions import AppException
from app.core.security import get_current_member
from app.repositories import menu as menu_repo
from app.repositories import objectlist as objectlist_repo
from app.schemas.objectlist import ObjectListPage

router = APIRouter(prefix="/menu", tags=["menu"], dependencies=[Depends(get_current_member)])


class MenuOut(BaseModel):
    cid: int
    name: str
    code: str
    mid: int
    # 給前端看的名稱；DB class.name 必須含 mid（insertClass 同名會撞到別人）
    label: str = "我的菜單"


class AddMenuItem(BaseModel):
    oid: int = Field(..., ge=1)


@router.get("/me", response_model=MenuOut)
def read_my_menu(member: dict = Depends(get_current_member)) -> dict:
    # label 只作 DB 唯一名素材；回傳給前端的顯示名固定「我的菜單」
    raw = member.get("display_name") or member.get("name") or f"user{member['id']}"
    menu = menu_repo.get_or_create_my_menu(member["id"], label=str(raw))
    menu["label"] = "我的菜單"
    return menu


@router.get("/me/items", response_model=ObjectListPage)
def list_my_menu_items(
    member: dict = Depends(get_current_member),
    page: int = 1,
    size: int = 50,
) -> dict:
    menu = menu_repo.get_or_create_my_menu(member["id"])
    return objectlist_repo.list_by_cid_page(menu["cid"], q=None, page=page, size=size)


@router.post("/me/items")
def add_menu_item(body: AddMenuItem, member: dict = Depends(get_current_member)) -> dict:
    result = menu_repo.add_to_menu(member["id"], body.oid)
    if not result.get("ok"):
        raise AppException(404, "找不到這個動作")
    return result


@router.delete("/me/items/{oid}")
def delete_menu_item(oid: int, member: dict = Depends(get_current_member)) -> dict:
    result = menu_repo.remove_from_menu(member["id"], oid)
    if not result.get("ok"):
        raise AppException(404, "菜單裡沒有這個動作")
    return result
