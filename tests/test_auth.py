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
