# Help with Swedish API

A small FastAPI service exposing the skill's channel, podcast, and speaking-clip
recommendations as JSON, filterable by CEFR level and skill — plus a live chat
endpoint that answers as the mentor itself.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | Query params |
|---|---|---|
| GET | `/health` | — |
| GET | `/levels` | — |
| GET | `/levels/guide` | — |
| GET | `/channels` | `level`, `skill` |
| GET | `/podcasts` | `level`, `skill` |
| GET | `/speaking-clips` | — |
| GET | `/recommendations` | `level` (required), `skill`, `limit` |
| GET | `/instructions` | — the mentor's rules, for your own model's system prompt |
| POST | `/chat` | the mentor talking for itself, via a free model on OpenRouter — off until `HWS_OPENROUTER_API_KEY` is set |

## Example

```bash
curl "http://127.0.0.1:8000/recommendations?level=A2&skill=listening"
```

### `POST /chat`

`{"message": "...", "history": [{"role": "user", "content": "..."}, ...]}` →
`{"reply": "..."}`. Stateless like every other route — `history` is the prior
turns, oldest first, and the caller resends it each time. The system prompt is
the same fenced block [`universal-prompt.md`](../universal-prompt.md) hands out
for copy-pasting into any AI chat, so a live chat answer never drifts from that
version — and `GET /instructions` returns the same text, for your own model.
The model gets one tool, `get_recommendations`, wired to the same data as
`GET /recommendations`, so it looks up a real channel or podcast instead of
inventing a name or URL.

Routed through [OpenRouter](https://openrouter.ai), not a provider directly —
`openai.OpenAI(base_url="https://openrouter.ai/api/v1")` against the model
slug `google/gemma-4-31b-it:free`, Google's Gemma 4 31B on OpenRouter's free
tier: no cost, tool calling, a 256K context window. Nothing calls the model
until `HWS_OPENROUTER_API_KEY` is set — a key-less deployment serves every
other route normally and returns `501` on this one alone. Get a key (no
payment needed for the free tier) at [openrouter.ai/keys](https://openrouter.ai/keys)
and set it as `HWS_OPENROUTER_API_KEY`, not the generic `OPENROUTER_API_KEY`
name — the prefix keeps it apart from any other app's OpenRouter key on the
same host or dashboard.

Free-tier models come and go on OpenRouter and carry their own upstream rate
limits — check [openrouter.ai/models](https://openrouter.ai/models?max_price=0)
if `HWS_CHAT_MODEL`'s default ever stops resolving, and swap in another
`:free` slug that lists `tools` under its supported parameters.

## Settings

All optional. The defaults suit a local run.

| Variable | Default | Does |
|---|---|---|
| `HWS_OPENROUTER_API_KEY` | unset (`/chat` returns 501) | Enables `POST /chat` — an OpenRouter key, not a Google one. Prefixed on purpose, not OpenRouter's own generic `OPENROUTER_API_KEY` name, so it can't get mixed up with another project's key |
| `HWS_CHAT_MODEL` | `google/gemma-4-31b-it:free` | OpenRouter model slug `/chat` calls |
| `HWS_CHAT_MAX_TOKENS` | `1024` | Max output tokens per chat reply |
| `HWS_CHAT_RATE_LIMIT_PER_MIN` | `6` | Chat turns per IP per minute, counted per instance |

If you point [`docs/index.html`](../docs/index.html)'s chat box at a deployed
instance that restricts CORS, allow that page's origin; this API ships with
`allow_origins=["*"]` so no extra setup is needed by default.

## Test

```bash
pip install -r requirements-dev.txt
pytest
```

The chat tests run without a key — they check the 501 fallback, the tool
function directly, and the rate limiter, none of which touch the network.

Data in `data.py` mirrors `../swedish_mentor/references/*.md`. Update both when adding sources.
