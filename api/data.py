"""Structured mirror of the reference data in hjälp_om_svenska/references/.

Kept in sync by hand with channels-by-level.md, podcasts-by-level.md, and
speaking-clips.md so the API and the Claude skill recommend the same sources.
"""

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

CHANNELS = [
    {
        "name": "Lätt Svenska med Oskar",
        "levels": ["A1", "A2", "B1"],
        "skills": ["listening", "speaking", "reading"],
        "description": "Natural slow speech, conversations, transcripts.",
    },
    {
        "name": "Svenska med Anastasia",
        "levels": ["A1", "A2"],
        "skills": ["listening", "speaking"],
        "description": "Beginner-friendly conversational Swedish.",
    },
    {
        "name": "Fun Swedish",
        "levels": ["A1", "A2"],
        "skills": ["listening", "speaking"],
        "description": "Beginner and mixed-level content.",
    },
    {
        "name": "Peter SFI",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["grammar", "pronunciation", "listening"],
        "description": "Grammar, uttal, SFI-style lessons.",
    },
    {
        "name": "UR Play (Studera svenska)",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["listening", "reading"],
        "description": "Structured educational clips.",
    },
    {
        "name": "Swedish Shadowing",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["speaking", "pronunciation"],
        "description": "Pronunciation and speaking drills.",
    },
]

PODCASTS = [
    {
        "name": "Radio Sweden på lätt svenska",
        "levels": ["A2", "B1"],
        "skills": ["listening", "reading"],
        "description": "Easy-Swedish news, slow and clear (SR).",
    },
    {
        "name": "Klartext",
        "levels": ["B1"],
        "skills": ["listening", "reading"],
        "description": "Simplified weekly news roundup (SR).",
    },
    {
        "name": "Fluent Fiction – Swedish",
        "levels": ["A2", "B1", "B2"],
        "skills": ["listening", "vocabulary"],
        "description": "Short story episodes with vocab recap.",
    },
    {
        "name": "P3 Dokumentär",
        "levels": ["B2", "C1", "C2"],
        "skills": ["listening"],
        "description": "Native-speed documentary storytelling.",
    },
    {
        "name": "Sommar i P1",
        "levels": ["B2", "C1", "C2"],
        "skills": ["listening"],
        "description": "Long-form native monologues, cultural depth.",
    },
]

SPEAKING_CLIPS = [
    {"description": "Shadowing drills", "source": "Swedish Shadowing"},
    {"description": "Short dialogues", "source": "Lätt Svenska med Oskar"},
    {"description": "Pronunciation practice", "source": "Peter SFI"},
    {"description": "Slow conversational clips", "source": "Svenska med Anastasia"},
]
