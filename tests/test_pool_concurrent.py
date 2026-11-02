"""W08：簡單並發煙霧測試（手動負載的縮小版）。"""
from concurrent.futures import ThreadPoolExecutor, as_completed


def test_health_under_concurrent_requests(client):
    def once(_):
        return client.get("/api/health").status_code

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(once, i) for i in range(24)]
        codes = [f.result() for f in as_completed(futures)]

    assert codes.count(200) == 24


def test_notes_list_concurrent_with_auth(auth_client):
    def once(_):
        return auth_client.get("/api/notes").status_code

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(once, i) for i in range(12)]
        codes = [f.result() for f in as_completed(futures)]

    assert all(code == 200 for code in codes)
