from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from data import CHANNELS, LEVELS, PODCASTS, SPEAKING_CLIPS

app = FastAPI(
    title="Help with Swedish API",
    description="Level-appropriate YouTube channels, podcasts, and speaking clips for Swedish learners.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/levels")
def get_levels():
    return LEVELS


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
    resources = [{**c, "type": "channel"} for c in CHANNELS] + [{**p, "type": "podcast"} for p in PODCASTS]
    return _filter(resources, level, skill)[:limit]
