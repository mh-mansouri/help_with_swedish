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
| POST | `/chat` | the mentor talking for itself, via OpenRouter (billed model, free fallback) — off until `HWS_OPENROUTER_API_KEY` is set |

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
`openai.OpenAI(base_url="https://openrouter.ai/api/v1")`. Nothing calls a
model until `HWS_OPENROUTER_API_KEY` is set — a key-less deployment serves
every other route normally and returns `501` on this one alone. Get a key at
[openrouter.ai/keys](https://openrouter.ai/keys) and set it as
`HWS_OPENROUTER_API_KEY`, not the generic `OPENROUTER_API_KEY` name — the
prefix keeps it apart from any other app's OpenRouter key on the same host
or dashboard.

**Two models, tried in order:**

1. `HWS_CHAT_MODEL`, default `anthropic/claude-sonnet-5` — the same model,
   over the same OpenRouter route, as the [embedded-iot-mentor](https://github.com/mh-mansouri/embedded-iot-mentor)
   sample this API's `/chat` was modeled on. Same per-token price as calling
   Anthropic directly — **billed, not free**, so it needs real credit on the
   OpenRouter account behind `HWS_OPENROUTER_API_KEY`. Chosen as the default
   because free-tier models on OpenRouter share throttled capacity and can be
   noticeably slower to reply.
2. `HWS_CHAT_FALLBACK_MODEL`, default `google/gemma-4-31b-it:free` — used
   automatically if the primary model is out of credit, rate-limited, or
   briefly unreachable, so the chat box degrades to slower-but-free instead
   of erroring. This was `/chat`'s only model before Claude was added. Set
   `HWS_CHAT_FALLBACK_MODEL=""` to disable the fallback entirely and let a
   primary-model failure surface as an error.

A fallback response is logged (`hws.chat`, on the server, not sent to the
caller) so you can tell from Render's logs when you're burning through free
capacity because the OpenRouter account is out of credit.

Free-tier models come and go on OpenRouter and carry their own upstream rate
limits — check [openrouter.ai/models](https://openrouter.ai/models?max_price=0)
if the fallback's default ever stops resolving, and swap in another `:free`
slug that lists `tools` under its supported parameters.

## Settings

All optional. The defaults suit a local run.

| Variable | Default | Does |
|---|---|---|
| `HWS_OPENROUTER_API_KEY` | unset (`/chat` returns 501) | Enables `POST /chat` — an OpenRouter key, not a Google or Anthropic one. Prefixed on purpose, not OpenRouter's own generic `OPENROUTER_API_KEY` name, so it can't get mixed up with another project's key |
| `HWS_CHAT_MODEL` | `anthropic/claude-sonnet-5` | Primary OpenRouter model slug `/chat` calls — billed |
| `HWS_CHAT_FALLBACK_MODEL` | `google/gemma-4-31b-it:free` | Used if the primary model fails; `""` disables the fallback |
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
