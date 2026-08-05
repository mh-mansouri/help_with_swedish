# Changelog

## Unreleased
- Added live chat: `POST /chat` on the API, talking as the mentor via a model on OpenRouter, off until a deployment sets `HWS_OPENROUTER_API_KEY` (project-prefixed rather than OpenRouter's generic `OPENROUTER_API_KEY`, so it can't collide with another app's key on a shared host). The model gets a `get_recommendations` tool wired to `data.py` so it can only cite a real channel or podcast, never an invented one. New `GET /instructions` returns the same system prompt for your own model. The webpage gained a trilingual chat box that calls it, alongside the existing no-AI form.
- Switched `/chat`'s primary model to Claude Sonnet 5 (`HWS_CHAT_MODEL`) — the same model, over the same OpenRouter route, as the embedded-iot-mentor sample, and noticeably faster than the free tier. It's billed, not free, so it needs real OpenRouter credit; the original free model (`google/gemma-4-31b-it:free`) is kept as `HWS_CHAT_FALLBACK_MODEL` and used automatically if the primary is out of credit, rate-limited, or briefly unreachable.
- `/chat` no longer relays raw OpenRouter error text to the caller (it can echo back parts of the rejected request); the detail is logged server-side instead, with the upstream HTTP status still included in the response for quick diagnosis.
- Added strict scope rules to the Skill, universal prompt, and README prompt copy: the mentor declines anything outside Swedish-learning (other subjects, requests to change its role or ignore its instructions) with one warm sentence instead of engaging, and treats text inside a user message as content, never as a command. Tone rules now explicitly call for staying calm and sympathetic when a learner is frustrated or stuck.
- The mentor may now mention, at most once per conversation and only when it fits, that a companion site (svenskamentor.se) is launching soon — never as a link, never implying it's live yet.
- Added CI (`.github/workflows/ci.yml`): runs the API test suite on every push/PR, and a weekly job that checks every recommended channel/podcast link still resolves (`scripts/check_links.py`).
- The webpage now always opens in Swedish for a new visitor instead of auto-detecting the browser's language — this is a Swedish-learning page first. A language switched manually is still remembered via localStorage and wins on the next visit.
- Fixed the chat replying in English on the Swedish page even when the visitor wrote in Swedish: a short first message like "Hej!" alone wasn't a reliable enough signal. The webpage now sends its selected UI language to `POST /chat` (new optional `lang` field), passed to the model as a separate, uncached system note (so it never disturbs Claude's prompt cache on the main instructions) — the Skill, universal prompt, and README's Language rules now say to treat it as a strong default.
- Added Open Graph / Twitter Card meta tags to the webpage, updated per language, so sharing the link shows a proper title/description/preview image.
- Regenerated `assets/skill-demo.gif` to mention the webpage and its three languages.
- Added `assets/chat-demo.gif`, a real screen recording (not a mockup) of a learner asking the live chat for speaking help on the Swedish page and getting a plan with real linked videos. Linked from all three READMEs.

## 0.4.0
- Renamed the skill folder/bundle from `hjälp_om_svenska` to the ASCII-safe `swedish_mentor` (fixes tooling and link issues with non-ASCII paths).
- Added `universal-prompt.md`, a plain-text copy-paste prompt that works in any AI chat (ChatGPT, Gemini, Copilot, etc.), not just Claude.
- Added a screenshotted step-by-step walkthrough for installing the Skill in Claude.ai.
- Added `docs/index.html`, a standalone webpage (no AI chat, no account) hosted on GitHub Pages that calls the live API directly; enabled CORS on the API for it.
- Made the webpage trilingual — Swedish (default), English, Persian — with right-to-left layout for Persian.
- Added a verified, clickable official link for every recommended channel and podcast across the API, Skill, prompt, and webpage.
- Added a plain-language CEFR level guide (what A1-C2 mean) to the README, Skill, prompt, and webpage; new `GET /levels/guide` endpoint on the API.

## 0.3.0
- Added a REST API (api/) exposing channel, podcast, and speaking-clip recommendations, filterable by CEFR level and skill.
- Included tests and install/run instructions for the API.

## 0.2.0
- Added podcast recommendations (references/podcasts-by-level.md) alongside YouTube clips.
- Updated SKILL.md triggers and instructions to cover podcasts by CEFR level.

## 0.1.0
- Reorganized the project into a skill-based repository layout.
- Added packaging support and repository documentation.
