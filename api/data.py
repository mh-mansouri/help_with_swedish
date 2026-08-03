"""Structured mirror of the reference data in swedish_mentor/references/.

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
        "url": "https://www.youtube.com/@LattSvenskaMedOskar",
    },
    {
        "name": "Svenska med Anastasia",
        "levels": ["A1", "A2"],
        "skills": ["listening", "speaking"],
        "description": "Beginner-friendly conversational Swedish.",
        "url": "https://www.youtube.com/@SvenskamedAnastasia",
    },
    {
        "name": "Fun Swedish",
        "levels": ["A1", "A2"],
        "skills": ["listening", "speaking"],
        "description": "Beginner and mixed-level content.",
        "url": "https://www.youtube.com/@FunSwedish",
    },
    {
        "name": "Peter SFI",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["grammar", "pronunciation", "listening"],
        "description": "Grammar, uttal, SFI-style lessons.",
        "url": "https://www.youtube.com/@petersfi6089",
    },
    {
        "name": "UR Play (Studera svenska)",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["listening", "reading"],
        "description": "Structured educational clips.",
        "url": "https://urplay.se/serie/232022-studera-svenska",
    },
    {
        "name": "Swedish Shadowing",
        "levels": ["B1", "B2", "C1", "C2"],
        "skills": ["speaking", "pronunciation"],
        "description": "Pronunciation and speaking drills.",
        "url": None,
    },
]

PODCASTS = [
    {
        "name": "Radio Sweden på lätt svenska",
        "levels": ["A2", "B1"],
        "skills": ["listening", "reading"],
        "description": "Easy-Swedish news, slow and clear (SR).",
        "url": "https://www.sverigesradio.se/radio-sweden-pa-latt-svenska",
    },
    {
        "name": "Klartext",
        "levels": ["B1"],
        "skills": ["listening", "reading"],
        "description": "Simplified weekly news roundup (SR).",
        "url": "https://www.sverigesradio.se/nyheter/klartext",
    },
    {
        "name": "Fluent Fiction – Swedish",
        "levels": ["A2", "B1", "B2"],
        "skills": ["listening", "vocabulary"],
        "description": "Short story episodes with vocab recap.",
        "url": "https://open.spotify.com/show/23FP4OW1aGtwFxwHTpSpE8",
    },
    {
        "name": "P3 Dokumentär",
        "levels": ["B2", "C1", "C2"],
        "skills": ["listening"],
        "description": "Native-speed documentary storytelling.",
        "url": "https://www.sverigesradio.se/p3dokumentar",
    },
    {
        "name": "Sommar i P1",
        "levels": ["B2", "C1", "C2"],
        "skills": ["listening"],
        "description": "Long-form native monologues, cultural depth.",
        "url": "https://www.sverigesradio.se/sommar-i-p1",
    },
]

LEVEL_GUIDE = [
    {"level": "A1", "name": "Beginner", "description": "Understand and use very basic phrases. Introduce yourself and ask simple questions."},
    {"level": "A2", "name": "Elementary", "description": "Handle simple, everyday exchanges like shopping, directions, and routines."},
    {"level": "B1", "name": "Intermediate", "description": "Manage most situations while traveling or at work. Describe experiences and plans."},
    {"level": "B2", "name": "Upper intermediate", "description": "Interact fluently with native speakers. Understand the main ideas of complex text."},
    {"level": "C1", "name": "Advanced", "description": "Express yourself fluently and spontaneously on demanding academic or professional topics."},
    {"level": "C2", "name": "Proficient", "description": "Understand virtually everything heard or read, with near-native fluency."},
]

SPEAKING_CLIPS = [
    {"description": "Shadowing drills", "source": "Swedish Shadowing"},
    {"description": "Short dialogues", "source": "Lätt Svenska med Oskar"},
    {"description": "Pronunciation practice", "source": "Peter SFI"},
    {"description": "Slow conversational clips", "source": "Svenska med Anastasia"},
]
