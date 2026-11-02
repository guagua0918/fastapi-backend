"""W07：TestClient fixtures。用 dependency override 模擬登入，不必真的走 Google。"""
import asyncio
import sys

# 須在 import app 前設定（與 main.py 相同：psycopg async on Windows）
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from fastapi.testclient import TestClient

from app.core.security import get_current_member
from app.main import app

FAKE_MEMBER = {
    "id": 1,
    "email": "pytest@example.com",
    "name": "Pytest User",
    "display_name": None,
    "picture": None,
}


@pytest.fixture
def client():
    """未登入的客戶端（不 override 身分）。"""
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client():
    """已登入：把 get_current_member 換成假會員。"""

    def _fake_member():
        return FAKE_MEMBER

    app.dependency_overrides[get_current_member] = _fake_member
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
