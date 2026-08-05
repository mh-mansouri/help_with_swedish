import json
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Literal, Optional

import openai
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from data import CHANNELS, LEVEL_GUIDE, LEVELS, PODCASTS, SPEAKING_CLIPS

HERE = Path(__file__).resolve().parent

# The same text a learner would copy-paste into any AI chat, reused as the
# system prompt so a live /chat answer never drifts from that version.
UNIVERSAL_PROMPT = HERE.parent / "universal-prompt.md"

# POST /chat is off until this is set — no key means no accidental spend, and
# every other route keeps working. Routed through OpenRouter rather than
# calling a provider directly, so this is an OpenRouter key
# (openrouter.ai/keys), not a Google one — the two are not interchangeable.
# Prefixed like the other settings below (HWS_) rather than the bare
# OPENROUTER_API_KEY OpenRouter's own docs suggest, so it can't collide with
# another app's key of the same generic name on a shared host or dashboard.
HWS_OPENROUTER_API_KEY = os.environ.get("HWS_OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# Claude Sonnet 5 — the same model, over the same OpenRouter route, as the
# embedded-iot-mentor sample. Same per-token price as calling Anthropic
# directly; billed, not free, so it needs real credit behind
# HWS_OPENROUTER_API_KEY. Chosen over the free tier below for speed: OpenRouter's
# free models share throttled capacity and can be noticeably slower to reply.
CHAT_MODEL = os.environ.get("HWS_CHAT_MODEL", "anthropic/claude-sonnet-5")
# Used automatically if the primary model has no credit, is rate-limited, or
# is briefly unreachable — the free model this API used exclusively before
# Claude was added. Set to "" to disable the fallback and let a primary
# failure surface as an error instead of silently switching models.
CHAT_FALLBACK_MODEL = os.environ.get("HWS_CHAT_FALLBACK_MODEL", "google/gemma-4-31b-it:free")
CHAT_MAX_TOKENS = int(os.environ.get("HWS_CHAT_MAX_TOKENS", "1024"))
CHAT_MAX_TOOL_ROUNDS = 4
# Its own bucket, tighter than a plain GET: a chat turn calls a billed model
# by default (with a free model as fallback), the other routes don't.
CHAT_RATE_LIMIT_PER_MIN = int(os.environ.get("HWS_CHAT_RATE_LIMIT_PER_MIN", "6"))

app = FastAPI(
    title="Help with Swedish API",
    description="Level-appropriate YouTube channels, podcasts, and speaking clips for Swedish learners.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _filter(resources: list[dict], level: Optional[str], skill: Optional[str]) -> list[dict]:
    result = resources
    if level:
        level = level.upper()
        if level not in LEVELS:
            raise HTTPException(status_code=400, detail=f"Unknown level '{level}'. Valid levels: {LEVELS}")
        result = [r for r in result if level in r["levels"]]
    if skill:
        skill = skill.lower()
        result = [r for r in result if skill in [s.lower() for s in r["skills"]]]
    return result


def _recommendations(level: Optional[str], skill: Optional[str], limit: int) -> list[dict]:
    resources = [{**c, "type": "channel"} for c in CHANNELS] + [{**p, "type": "podcast"} for p in PODCASTS]
    return _filter(resources, level, skill)[:limit]


def load_chat_instructions() -> str:
    """The universal copy-paste prompt's fenced block, verbatim — the same
    text a learner would paste as the first message into any AI chat, reused
    as /chat's system prompt so a live answer never drifts from that version."""
    if not UNIVERSAL_PROMPT.is_file():
        raise HTTPException(500, f"instructions missing: {UNIVERSAL_PROMPT}")
    text = UNIVERSAL_PROMPT.read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)\n```", text, re.DOTALL)
    if not match:
        raise HTTPException(500, f"could not find fenced prompt in {UNIVERSAL_PROMPT}")
    return match.group(1)


def _system_message(cache: bool) -> dict:
    text = load_chat_instructions()
    if not cache:
        return {"role": "system", "content": text}
    # Anthropic-style prompt caching, passed through by OpenRouter: the
    # instructions never change within a deployment's lifetime, so every
    # caller after the first reads this from cache instead of paying full
    # price for it again. Only meaningful for the primary (Claude) model.
    return {
        "role": "system",
        "content": [{
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral"},
        }],
    }


_chat_client: openai.OpenAI | None = None


def _chat_client_or_501() -> openai.OpenAI:
    """Lazy singleton so a key-less deployment never touches the SDK.
    OpenRouter speaks the OpenAI Chat Completions shape, so this is an
    openai.OpenAI client pointed at OpenRouter's base URL."""
    global _chat_client
    if not HWS_OPENROUTER_API_KEY:
        raise HTTPException(501, "chat is not configured on this server: set HWS_OPENROUTER_API_KEY")
    if _chat_client is None:
        _chat_client = openai.OpenAI(
            api_key=HWS_OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/mh-mansouri/help_with_swedish",
                "X-Title": "Help with Swedish",
            },
        )
    return _chat_client


# Model-availability problems worth retrying on the fallback model: no credit
# left, rate-limited, a slug that stopped resolving, or a brief network blip.
# AuthenticationError is deliberately not here — a rejected key fails the
# same way on both models, so retrying would just waste a call.
_FALLBACK_ELIGIBLE = (
    openai.NotFoundError,
    openai.RateLimitError,
    openai.APIStatusError,
    openai.APIConnectionError,
)


def _chat_turn(client: openai.OpenAI, model: str, history_messages: list[dict], user_message: dict, cache: bool):
    """Run one full tool-calling turn against a single model and return the
    final choice. Raises the openai SDK's own exceptions on failure — the
    caller decides whether that means falling back to another model."""
    messages: list[dict] = [_system_message(cache), *history_messages, user_message]
    for _ in range(CHAT_MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=model,
            max_tokens=CHAT_MAX_TOKENS,
            messages=messages,
            tools=CHAT_TOOLS,
        )
        choice = response.choices[0]
        if choice.finish_reason != "tool_calls" or not choice.message.tool_calls:
            return choice
        messages.append(choice.message.model_dump(exclude_none=True))
        for call in choice.message.tool_calls:
            try:
                args = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                content = f"error: malformed arguments — {call.function.arguments!r}"
            else:
                content, _is_error = _run_chat_tool(call.function.name, args)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": content})
    raise HTTPException(504, "chat: too many tool calls in one turn")


def _chat_completion(client: openai.OpenAI, history_messages: list[dict], user_message: dict) -> tuple[str, object]:
    """Try the primary model; on a model-availability problem, retry once on
    the free fallback model rather than surfacing an error straight to the
    caller. Returns (model actually used, final choice)."""
    try:
        return CHAT_MODEL, _chat_turn(client, CHAT_MODEL, history_messages, user_message, cache=True)
    except _FALLBACK_ELIGIBLE:
        if not CHAT_FALLBACK_MODEL:
            raise
        return CHAT_FALLBACK_MODEL, _chat_turn(client, CHAT_FALLBACK_MODEL, history_messages, user_message, cache=False)


# Offered as a tool rather than left to the model's memory, so a live chat
# reply can only cite a channel or podcast that is actually in data.py — the
# same rule the skill and the universal prompt already state in words.
CHAT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_recommendations",
            "description": (
                "Look up real, verified YouTube channels and podcasts for a CEFR "
                "level and optional skill. Always call this before naming a "
                "channel, podcast, or link — never invent one from memory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {"type": "string", "enum": LEVELS, "description": "CEFR level, e.g. A2"},
                    "skill": {
                        "type": "string",
                        "description": "listening, speaking, reading, writing, grammar, pronunciation, or vocabulary",
                    },
                    "limit": {"type": "integer", "minimum": 1, "maximum": 20, "description": "default 6"},
                },
                "required": ["level"],
            },
        },
    },
]


def _run_chat_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Run one chat tool call through the same data and filter the REST
    routes use, so a chat answer and a direct API call never disagree.
    Returns (content, is_error) — errors go back to the model as text, not
    raised, so it can explain the problem instead of the turn just failing."""
    if name != "get_recommendations":
        return f"error: unknown tool '{name}'", True
    try:
        limit = int(tool_input.get("limit", 6))
        items = _recommendations(tool_input.get("level"), tool_input.get("skill"), max(1, min(limit, 20)))
    except HTTPException as exc:
        return f"error: {exc.detail}", True
    return json.dumps(items, ensure_ascii=False), False


_chat_hits: dict[str, list[float]] = {}
_chat_hits_lock = threading.Lock()


def _client_ip(request: Request) -> str:
    # Render and most hosts terminate TLS in front, so the socket peer is the
    # proxy and every caller would share one bucket. The first hop in
    # X-Forwarded-For is the real client.
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded.strip():
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _within_chat_rate_limit(ip: str) -> bool:
    """Fixed one-minute window, per process. Good enough for one small
    instance; a second instance would need shared state, which is not worth
    a Redis for a free-tier chat box."""
    now = time.monotonic()
    with _chat_hits_lock:
        recent = [t for t in _chat_hits.get(ip, ()) if now - t < 60]
        if len(recent) >= CHAT_RATE_LIMIT_PER_MIN:
            _chat_hits[ip] = recent
            return False
        recent.append(now)
        _chat_hits[ip] = recent
        return True


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    # Prior turns, oldest first; the client resends them each time since the
    # API itself keeps no session state.
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/levels")
def get_levels():
    return LEVELS


@app.get("/levels/guide")
def get_levels_guide():
    return LEVEL_GUIDE


@app.get("/channels")
def get_channels(
    level: Optional[str] = Query(None, description="CEFR level, e.g. A2"),
    skill: Optional[str] = Query(None, description="listening, speaking, reading, writing, grammar, pronunciation, vocabulary"),
):
    return _filter(CHANNELS, level, skill)


@app.get("/podcasts")
def get_podcasts(
    level: Optional[str] = Query(None, description="CEFR level, e.g. A2"),
    skill: Optional[str] = Query(None, description="listening, speaking, reading, writing, grammar, pronunciation, vocabulary"),
):
    return _filter(PODCASTS, level, skill)


@app.get("/speaking-clips")
def get_speaking_clips():
    return SPEAKING_CLIPS


@app.get("/recommendations")
def get_recommendations(
    level: str = Query(..., description="CEFR level, e.g. A2"),
    skill: Optional[str] = Query(None, description="listening, speaking, reading, writing, grammar, pronunciation, vocabulary"),
    limit: int = Query(5, ge=1, le=20),
):
    return _recommendations(level, skill, limit)


@app.get("/instructions")
def get_instructions():
    """The mentor's rules, for your own model's system prompt — the same text
    POST /chat below uses."""
    return {"instructions": load_chat_instructions()}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request) -> ChatResponse:
    """The mentor talking for itself: same rules and resource library as the
    Skill and the universal prompt, but a model on OpenRouter does the talking
    instead of a human copy-pasting into a chat app. Tries the primary
    (billed) model first and falls back to a free model if that one is
    unavailable — see CHAT_MODEL / CHAT_FALLBACK_MODEL."""
    if not _within_chat_rate_limit(_client_ip(request)):
        raise HTTPException(429, "chat rate limit exceeded — try again in a minute",
                             headers={"Retry-After": "60"})

    client = _chat_client_or_501()
    history_messages = [{"role": m.role, "content": m.content} for m in req.history]
    user_message = {"role": "user", "content": req.message}

    try:
        model_used, choice = _chat_completion(client, history_messages, user_message)
    except openai.AuthenticationError as exc:
        raise HTTPException(500, "chat: HWS_OPENROUTER_API_KEY was rejected — check it's set correctly") from exc
    except openai.NotFoundError as exc:
        raise HTTPException(500, "chat: no configured model resolved on OpenRouter — "
                                  "check HWS_CHAT_MODEL and HWS_CHAT_FALLBACK_MODEL") from exc
    except openai.RateLimitError as exc:
        raise HTTPException(429, "chat: upstream rate limit hit, try again shortly",
                             headers={"Retry-After": "30"}) from exc
    except openai.APIStatusError as exc:
        # exc.message can echo back parts of the request OpenRouter rejected
        # (e.g. an invalid model slug) — logged for the operator, not relayed
        # to the caller, so a misconfigured secret can't leak through here.
        logging.getLogger("hws.chat").error("OpenRouter API error (%s): %s", exc.status_code, exc.message)
        raise HTTPException(502, f"chat: OpenRouter API error (upstream status {exc.status_code}) — "
                                  "check the server logs and HWS_CHAT_MODEL/HWS_CHAT_FALLBACK_MODEL") from exc
    except openai.APIConnectionError as exc:
        raise HTTPException(502, "chat: could not reach OpenRouter") from exc

    if model_used != CHAT_MODEL:
        logging.getLogger("hws.chat").warning(
            "primary model %s unavailable, served via fallback %s", CHAT_MODEL, model_used,
        )

    if choice.finish_reason == "content_filter":
        raise HTTPException(422, "the model declined to answer that")

    reply = (choice.message.content or "").strip()
    return ChatResponse(reply=reply or "(no response)")
