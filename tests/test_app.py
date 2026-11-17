import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app  # noqa: E402


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_message():
    client = app.test_client()
    res = client.get("/api/message")
    assert res.status_code == 200
    assert "Flask" in res.get_json()["message"]
