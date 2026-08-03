from fastapi.testclient import TestClient

from data import LEVELS
from main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_levels():
    assert "A2" in client.get("/levels").json()


def test_channels_filtered_by_level():
    resp = client.get("/channels", params={"level": "A2"})
    assert resp.status_code == 200
    names = [c["name"] for c in resp.json()]
    assert "Lätt Svenska med Oskar" in names
    assert "Peter SFI" not in names


def test_podcasts_filtered_by_skill():
    resp = client.get("/podcasts", params={"skill": "vocabulary"})
    assert resp.status_code == 200
    names = [p["name"] for p in resp.json()]
    assert names == ["Fluent Fiction – Swedish"]


def test_invalid_level():
    resp = client.get("/channels", params={"level": "Z9"})
    assert resp.status_code == 400


def test_recommendations_mix_channels_and_podcasts():
    resp = client.get("/recommendations", params={"level": "B1", "limit": 20})
    assert resp.status_code == 200
    types = {r["type"] for r in resp.json()}
    assert types == {"channel", "podcast"}


def test_recommendations_include_urls():
    resp = client.get("/recommendations", params={"level": "A2", "limit": 20})
    assert resp.status_code == 200
    by_name = {r["name"]: r["url"] for r in resp.json()}
    assert by_name["Lätt Svenska med Oskar"].startswith("https://")
    assert by_name["Radio Sweden på lätt svenska"].startswith("https://")


def test_levels_guide_covers_all_levels():
    resp = client.get("/levels/guide")
    assert resp.status_code == 200
    guide = resp.json()
    assert [g["level"] for g in guide] == LEVELS
    assert all(g["description"] for g in guide)
