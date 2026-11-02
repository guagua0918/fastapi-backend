"""Auth：對應講義「/register /login」——專案改測 Google JWT 門禁。"""
from app.core.security import COOKIE_NAME, create_access_token


def test_me_without_token_returns_401(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_subclass_without_token_returns_401(client):
    response = client.get("/api/subclass/pcid/1")
    assert response.status_code == 401


def test_notes_without_token_returns_401(client):
    response = client.get("/api/notes")
    assert response.status_code == 401


def test_invalid_token_returns_401(client):
    """對應講義「密碼錯誤」：壞掉的票也不能進。"""
    response = client.get(
        "/api/auth/me",
        cookies={COOKIE_NAME: "not.a.real.jwt"},
    )
    assert response.status_code == 401


def test_me_with_override_returns_profile(auth_client):
    response = auth_client.get("/api/auth/me")
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "pytest@example.com"
    assert body["name"] == "Pytest User"


def test_create_access_token_shape():
    """單元測：JWT 能簽出發、含 sub。"""
    token = create_access_token(1)
    assert isinstance(token, str)
    assert token.count(".") == 2


def test_patch_me_requires_auth(client):
    response = client.patch(
        "/api/auth/me",
        json={"display_name": "小幫手"},
    )
    assert response.status_code == 401


def test_patch_me_updates_display_name(auth_client, monkeypatch):
    """override 登入後，repository 層用假更新（不強制寫入開發庫）。"""
    from app.routers import auth as auth_router

    def fake_update(member_id, display_name):
        return {
            "id": member_id,
            "email": "pytest@example.com",
            "name": "Google Name",
            "display_name": display_name,
            "picture": None,
        }

    monkeypatch.setattr(auth_router.member_repo, "update_display_name", fake_update)
    response = auth_client.patch("/api/auth/me", json={"display_name": "足弓測試"})
    assert response.status_code == 200
    body = response.json()
    assert body["display_name"] == "足弓測試"
    assert body["name"] == "Google Name"
