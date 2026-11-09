"""W10：統一錯誤格式、未預期例外不洩漏 stack。"""

from fastapi.testclient import TestClient

from app.core.security import get_current_member
from app.main import app


def test_http_exception_shape_on_me_without_auth():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    body = response.json()
    assert "error" in body
    assert body["path"] == "/api/auth/me"
    assert "traceback" not in body
    assert "Traceback" not in response.text


def test_app_exception_object_not_found():
    app.dependency_overrides[get_current_member] = lambda: {"id": 1}
    client = TestClient(app, raise_server_exceptions=False)
    try:
        response = client.get("/api/object/oid/999999")
        assert response.status_code == 404
        body = response.json()
        assert body["error"] == "找不到這個物件"
        assert body["path"] == "/api/object/oid/999999"
    finally:
        app.dependency_overrides.clear()


def test_unhandled_exception_hides_details():
    from app.repositories import objectlist as objectlist_repo

    original = objectlist_repo.get_by_oid

    def boom(_oid: int):
        raise RuntimeError("secret-stack-should-not-leak")

    objectlist_repo.get_by_oid = boom  # type: ignore[method-assign]
    app.dependency_overrides[get_current_member] = lambda: {"id": 1}
    client = TestClient(app, raise_server_exceptions=False)
    try:
        response = client.get("/api/object/oid/1")
        assert response.status_code == 500
        body = response.json()
        assert body["error"] == "Internal server error"
        assert "secret-stack" not in response.text
        assert "RuntimeError" not in response.text
    finally:
        objectlist_repo.get_by_oid = original  # type: ignore[method-assign]
        app.dependency_overrides.clear()
