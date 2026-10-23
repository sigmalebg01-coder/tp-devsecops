from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_orders_ok(monkeypatch):
    monkeypatch.setenv("SIMULATE_FAILURE", "false")
    assert client.get("/orders").status_code == 200


def test_orders_failure_mode_returns_500(monkeypatch):
    monkeypatch.setenv("SIMULATE_FAILURE", "true")
    response = client.get("/orders")
    assert response.status_code == 500
    assert response.json()["error"] == "db_connection_timeout"


def test_metrics_exposed():
    client.get("/health")
    assert "http_requests_total" in client.get("/metrics").text