from pydantic import BaseModel


class SubclassItem(BaseModel):
    pcid: int
    parent_name: str
    cid: int
    child_name: str
