from fastapi.testclient import TestClient

from figure_store.main import app

client = TestClient(app)


def test_home_renders():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Figuras de anime originales" in response.text


def test_static_css_is_served():
    response = client.get("/static/css/styles.css")
    assert response.status_code == 200


def test_health():
    assert client.get("/health").json() == {"status": "ok"}
