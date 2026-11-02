"""Notes CRUD（需登入）。會真的打開發用 DB；測完會刪掉自己建的 note。"""


def test_create_and_get_note(auth_client):
    created = auth_client.post(
        "/api/notes",
        json={"title": "pytest-note", "content": "hello w07"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "pytest-note"
    note_id = body["id"]

    fetched = auth_client.get(f"/api/notes/{note_id}")
    assert fetched.status_code == 200
    assert fetched.json()["content"] == "hello w07"

    deleted = auth_client.delete(f"/api/notes/{note_id}")
    assert deleted.status_code == 204


def test_get_nonexistent_note_returns_404(auth_client):
    response = auth_client.get("/api/notes/999999")
    assert response.status_code == 404


def test_update_note(auth_client):
    created = auth_client.post(
        "/api/notes",
        json={"title": "before", "content": "a"},
    )
    note_id = created.json()["id"]

    updated = auth_client.put(
        f"/api/notes/{note_id}",
        json={"title": "after", "content": "b"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "after"

    auth_client.delete(f"/api/notes/{note_id}")


def test_delete_nonexistent_note_returns_404(auth_client):
    response = auth_client.delete("/api/notes/999999")
    assert response.status_code == 404


def test_list_notes_requires_auth(client):
    """未登入不能列 notes（Auth 門禁）。"""
    assert client.get("/api/notes").status_code == 401
