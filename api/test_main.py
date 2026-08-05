import json

import httpx
import openai
import pytest
from fastapi.testclient import TestClient

import main
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


def test_instructions_include_the_persona():
    resp = client.get("/instructions")
    assert resp.status_code == 200
    assert "Swedish YouTube & Podcast Mentor" in resp.json()["instructions"]


def test_chat_off_without_api_key():
    assert main.HWS_OPENROUTER_API_KEY == ""
    resp = client.post("/chat", json={"message": "hej"})
    assert resp.status_code == 501


def test_chat_model_matches_the_sample_with_a_free_fallback():
    # Same model, same OpenRouter route, as the embedded-iot-mentor sample —
    # billed, not free, hence the fallback below for when it's unavailable.
    assert main.CHAT_MODEL == "anthropic/claude-sonnet-5"
    assert main.CHAT_FALLBACK_MODEL.endswith(":free")
    assert main.CHAT_FALLBACK_MODEL.startswith("google/")


def test_chat_rejects_empty_message():
    resp = client.post("/chat", json={"message": ""})
    assert resp.status_code == 422


class _FakeMessage:
    def __init__(self, content):
        self.content = content
        self.tool_calls = None


class _FakeChoice:
    def __init__(self, content):
        self.finish_reason = "stop"
        self.message = _FakeMessage(content)


def _connection_error() -> openai.APIConnectionError:
    # No credit / rate limit / not found all need a fabricated httpx.Response;
    # APIConnectionError only needs a request, so it's the simplest stand-in
    # for "the primary model call failed" in these offline tests.
    return openai.APIConnectionError(request=httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions"))


def test_chat_completion_falls_back_when_primary_model_fails(monkeypatch):
    calls = []

    def fake_chat_turn(client, model, history_messages, user_message, cache, lang_hint=None):
        calls.append(model)
        if model == main.CHAT_MODEL:
            raise _connection_error()
        return _FakeChoice("fallback reply")

    monkeypatch.setattr(main, "_chat_turn", fake_chat_turn)
    model_used, choice = main._chat_completion(object(), [], {"role": "user", "content": "hej"})

    assert calls == [main.CHAT_MODEL, main.CHAT_FALLBACK_MODEL]
    assert model_used == main.CHAT_FALLBACK_MODEL
    assert choice.message.content == "fallback reply"


class _FakeCompletions:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return type("Resp", (), {"choices": [_FakeChoice("ok")]})()


class _FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {"completions": _FakeCompletions()})()


def test_chat_ui_langs_cover_the_pages_three_languages():
    assert main.CHAT_UI_LANGS == {"sv": "Swedish", "en": "English", "fa": "Persian"}


def test_chat_turn_sends_language_hint_as_its_own_uncached_message():
    fake = _FakeClient()
    main._chat_turn(fake, main.CHAT_MODEL, [], {"role": "user", "content": "Hej!"}, cache=True, lang_hint="Swedish")
    messages = fake.chat.completions.calls[0]["messages"]
    system_messages = [m for m in messages if m["role"] == "system"]
    assert len(system_messages) == 2
    assert "Swedish" in system_messages[1]["content"]
    # A plain string, not the cached content-block shape the first (real
    # instructions) system message uses — the hint must never touch the cache.
    assert isinstance(system_messages[1]["content"], str)


def test_chat_turn_omits_language_hint_when_none_given():
    fake = _FakeClient()
    main._chat_turn(fake, main.CHAT_MODEL, [], {"role": "user", "content": "Hej!"}, cache=True)
    messages = fake.chat.completions.calls[0]["messages"]
    assert len([m for m in messages if m["role"] == "system"]) == 1


def test_chat_completion_reraises_when_fallback_disabled(monkeypatch):
    monkeypatch.setattr(main, "_chat_turn", lambda *a, **k: (_ for _ in ()).throw(_connection_error()))
    original_fallback = main.CHAT_FALLBACK_MODEL
    main.CHAT_FALLBACK_MODEL = ""
    try:
        with pytest.raises(openai.APIConnectionError):
            main._chat_completion(object(), [], {"role": "user", "content": "hej"})
    finally:
        main.CHAT_FALLBACK_MODEL = original_fallback


def test_chat_tool_matches_the_recommendations_route():
    out, is_error = main._run_chat_tool("get_recommendations", {"level": "A2", "skill": "listening", "limit": 3})
    assert not is_error
    route_names = {r["name"] for r in main._recommendations("A2", "listening", 3)}
    assert {r["name"] for r in json.loads(out)} == route_names


def test_chat_tool_reports_unknown_tool():
    out, is_error = main._run_chat_tool("not_a_real_tool", {})
    assert is_error
    assert "not_a_real_tool" in out


def test_chat_tool_reports_bad_level_as_text_not_exception():
    out, is_error = main._run_chat_tool("get_recommendations", {"level": "Z9"})
    assert is_error
    assert "error:" in out


def test_chat_rate_limit_is_its_own_bucket():
    original_limit = main.CHAT_RATE_LIMIT_PER_MIN
    main.CHAT_RATE_LIMIT_PER_MIN = 2
    try:
        ip = "198.51.100.11"  # documentation range, so no real bucket is disturbed
        allowed = [main._within_chat_rate_limit(ip) for _ in range(4)]
        assert allowed == [True, True, False, False]
    finally:
        main.CHAT_RATE_LIMIT_PER_MIN = original_limit
        main._chat_hits.clear()


def test_client_ip_prefers_forwarded_header():
    class FakeRequest:
        headers = {"x-forwarded-for": "203.0.113.7, 10.0.0.1"}
        client = type("C", (), {"host": "10.0.0.1"})()

    assert main._client_ip(FakeRequest()) == "203.0.113.7"
