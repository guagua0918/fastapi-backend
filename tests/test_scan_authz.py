"""
練習不能刪別人的note在專案的對應：
notes 目前沒有 mid 欄位，所以改測 scan——別人的 session / footprint 不能動。
"""


def test_complete_unknown_session_returns_404(auth_client):
    response = auth_client.post("/api/scan/sessions/999999/complete")
    assert response.status_code == 404


def test_read_unknown_footprint_returns_404(auth_client):
    response = auth_client.get("/api/scan/footprints/999999")
    assert response.status_code == 404


def test_upload_requires_auth(client):
    response = client.post("/api/scan/sessions/1/feet/left")
    assert response.status_code == 401
