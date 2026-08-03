# Help with Swedish — a Claude Skill

English · [Svenska](README.sv.md) · [فارسی](README.fa.md)

A Claude Skill for helping Swedish learners find practical, level-appropriate YouTube clips and build a simple learning path.

Most language-learning advice is either too vague or too overwhelming. This skill helps by asking what the learner wants to improve, what level they are at, and then suggesting focused resources instead of random videos.

## Use it in 30 seconds

1. Download [hjälp_om_svenska.skill](hjälp_om_svenska.skill).
2. Open it in Claude.
3. Ask for a learning plan, for example: “I am A2 and want to improve my speaking before a trip to Sweden.”

## Demo

A learner says: “I am A2 and want to improve my speaking before a trip to Sweden.” The skill responds with a short plan, a few good video options, and a clearer next step.

![Skill demo GIF](assets/skill-demo.gif)

## What it does

- Picks a learning path based on level, goal, and skill area.
- Recommends YouTube clips for listening, reading, writing, and speaking.
- Prioritizes practical channels such as Peter SFI, Lätt Svenska med Oskar, UR Play, and Swedish Shadowing.
- Keeps guidance short, encouraging, and focused on one small step at a time.

## Why it exists

Many learners waste time watching unrelated videos or choosing content that is too hard or too easy. This skill helps them avoid that by offering manageable recommendations and a realistic path forward.

## Install

Option A — one file: download [hjälp_om_svenska.skill](hjälp_om_svenska.skill) and open it in Claude.

Option B — package it locally:

```bash
python package_skill.py
python package_skill.py --check
python package_skill.py --install --skills-dir <path-to-skills-folder>
```

The `--check` command validates that the required skill files are present before you use the bundle.

## Use it

Try prompts such as:

- “I want to improve my Swedish listening for everyday conversations.”
- “I am a beginner and want a simple speaking plan.”
- “Give me good Swedish videos for B1 reading practice.”
- “I want a 2-week plan for learning Swedish for work.”
- “I am A2 and want to improve my vocabulary before moving to Sweden.”
- “I think I’m intermediate at Swedish, but I’m not sure where I really belong.”

A good response usually includes:

- a short level check or suggestion,
- 3–5 video or playlist recommendations,
- and one clear next step for the learner.

A strong example looks like this:

> “You seem to be around A2. A good next step is listening practice and short speaking drills. I recommend three short clips and one daily routine.”

## What it helps with

- Choosing a good next step for Swedish learning
- Matching the learner to a level-appropriate path
- Suggesting practical YouTube resources without overwhelming the learner

## What it does not replace

- A formal language assessment
- A teacher-led placement test
- A guaranteed CEFR score

## Layout

- hjälp_om_svenska/SKILL.md — the skill instructions
- hjälp_om_svenska/references/ — reference files with channel and speaking examples
- hjälp_om_svenska.skill — the packaged skill bundle
- package_skill.py — builds the bundle

## Build

Run:

```bash
python package_skill.py
```

## Contributing

Improvements are welcome. If you have better channel suggestions, clearer examples, or stronger guidance, feel free to contribute.

## License

This project is released under the MIT License.

## About

This repository packages a Claude Skill for Swedish learners who want practical, level-based recommendations without feeling overwhelmed.
