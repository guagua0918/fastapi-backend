from pydantic import BaseModel, Field


class MemberProfile(BaseModel):
    id: int
    email: str
    name: str | None = Field(default=None, description="Google OAuth 姓名，設定頁不改")
    display_name: str | None = Field(default=None, description="使用者自訂顯示名稱")
    picture: str | None = None


class MemberProfileUpdate(BaseModel):
    display_name: str = Field(min_length=2, max_length=40)
