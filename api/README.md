# Help with Swedish API

A small FastAPI service exposing the skill's channel, podcast, and speaking-clip
recommendations as JSON, filterable by CEFR level and skill.

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
| GET | `/channels` | `level`, `skill` |
| GET | `/podcasts` | `level`, `skill` |
| GET | `/speaking-clips` | — |
| GET | `/recommendations` | `level` (required), `skill`, `limit` |

## Example

```bash
curl "http://127.0.0.1:8000/recommendations?level=A2&skill=listening"
```

## Test

```bash
pip install -r requirements-dev.txt
pytest
```

Data in `data.py` mirrors `../swedish_mentor/references/*.md`. Update both when adding sources.
