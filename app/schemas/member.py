from pydantic import BaseModel


class MemberProfile(BaseModel):
    id: int
    email: str
    name: str | None = None
    picture: str | None = None
