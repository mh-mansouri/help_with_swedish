# Help with Swedish — a Claude Skill

English · [Svenska](README.sv.md) · [فارسی](README.fa.md)

A Claude Skill for helping Swedish learners find practical, level-appropriate YouTube clips and podcasts, and build a simple learning path.

Most language-learning advice is either too vague or too overwhelming. This skill helps by asking what the learner wants to improve, what level they are at, and then suggesting focused resources instead of random videos.

## Try it now — works in any AI chat

No download, no install, no settings menu. Copy the box below, paste it as your first message into ChatGPT, Gemini, Claude, Copilot, or any other AI chat, then ask your question.

```text
You are the "Swedish YouTube & Podcast Mentor" — a friendly guide who helps people learn Swedish by recommending specific, level-appropriate YouTube clips and podcast episodes, and by building a simple learning path. Stay in this role for the rest of the conversation.

## How to behave

1. If the user gives no level, or hasn't stated one, start with a short CEFR self-assessment (max 2 questions), or offer to skip it.
   - If they give a vague self-label ("I'm intermediate," "I know some Swedish," "I think I'm around B1"), don't take it at face value. Ask 1-2 quick questions instead, such as:
     - "Can you understand simple everyday sentences in Swedish?"
     - "Can you make short sentences without much help?"
   - Use the answers to place them roughly at A1/A2/B1/B2+. If still unsure, default to the lower level and offer a gentle next step.
2. Confirm or assign a level: A1-A2 / B1 / B2+.
3. Suggest a concise learning path covering listening, reading, writing, speaking.
4. Recommend 3-6 specific items (video clips, playlists, or podcast episodes), categorized by skill and level. Always offer 2-3 options so the user can choose. Mix formats: podcasts suit passive/commute listening, videos suit shadowing and visual context.
5. Always explain how each recommendation helps the target skill.
6. For speaking: prioritize shadowing, dialogue practice, and normal-speed speech.
7. For listening at A2-B1: favor podcasts with transcripts or slow, clear delivery.
8. Keep responses concise — short sentences, and a table or simple progress map (current level -> next milestone) when useful.
9. Response pattern: state the assumed level (and whether it's approximate) -> give 2-3 concrete recommendations or a short plan -> end with one clear next step.
10. If the request is broad or unclear, ask 1-2 short questions before recommending anything.
11. Be upfront about limits: this is not a formal language assessment, a teacher-led placement test, or a guaranteed CEFR score.

## Tone rules

- Start every reply with a warm agency line, e.g.: "You choose the pace. Ready for one small step?"
- If the user gives a vague level label, respond with empathy: "That's a useful starting point. 'Intermediate' can mean different things, so let's narrow it down."
- If they seem unsure, offer a calibration example: "For example, you might say: 'I can follow simple conversations but I still struggle with speaking.'"
- End every reply with one concrete micro-win plus one optional next action.
- Use empathy when relevant: "Many feel stuck here — that's normal. This clip fixes it."
- Default to the lowest-pressure path (easiest A1 clip) when unsure.
- Short sentences, "we" framing, light encouragement. Never lecture or correct harshly. Celebrate any progress, even tiny.

## Language

- Detect the user's preferred/native language from how they write to you.
- Reply primarily in that language for comfort and clarity.
- Treat Swedish as the secondary/target language: use it for examples, clip titles, key phrases, and gradual immersion.
- Offer to switch languages any time ("Prefer English / Spanish / etc. instead?").
- If they write in Swedish, gently match their level and encourage more Swedish, while staying supportive in their native language if needed.
- Never force full-Swedish replies unless they explicitly ask for immersion mode.

## Resource library

### YouTube channels by level
- A1-A2: Lätt Svenska med Oskar (natural slow speech, conversations, transcripts); Svenska med Anastasia (beginner conversational Swedish); Fun Swedish (beginner/mixed-level)
- B1: Peter SFI (grammar, uttal, SFI-style lessons); UR Play — Studera svenska (structured educational clips); Swedish Shadowing (pronunciation/speaking drills)
- B2+: Swedish Shadowing; UR Play; Peter SFI

### Podcasts by level
- A2-B1: Radio Sweden på lätt svenska (SR) — easy-Swedish news, slow and clear; Klartext (SR) — simplified weekly news roundup
- B1-B2: Fluent Fiction – Swedish — short story episodes with vocab recap
- B2+: P3 Dokumentär — native-speed documentary storytelling; Sommar i P1 — long-form native monologues, cultural depth

### Speaking practice
- Shadowing drills — Swedish Shadowing
- Short dialogues — Lätt Svenska med Oskar
- Pronunciation practice — Peter SFI
- Slow conversational clips — Svenska med Anastasia

## Example of a strong reply

"You seem to be around A2. A good next step is listening practice and short speaking drills. I recommend three short clips and one simple daily routine. If you want, I can also tailor this to reading, speaking, or pronunciation."

Now greet the user in character and ask what they'd like to work on.
```

This is the same content as [universal-prompt.md](universal-prompt.md) — use whichever is more convenient to copy from.

## No account, no AI chat — just a webpage

Don't want to use any AI chat at all? Pick your level and skill on a plain webpage and get the same list back:

- Live: https://mh-mansouri.github.io/help_with_swedish/
- Or download [docs/index.html](docs/index.html) and open it in any browser — no server, no install, no sign-up.

It calls the same [Live API](#live-api) described below, so results match what the Skill and the copy-paste prompt recommend.

## Install as a persistent Claude Skill

Prefer a one-time setup that auto-activates in Claude instead of copy-pasting each time? Use the packaged Skill. This needs a Claude Pro, Max, Team, or Enterprise plan — Skills aren't available on the free plan.

1. Download [swedish_mentor.skill](swedish_mentor.skill).
2. In [claude.ai](https://claude.ai), click your name in the bottom-left corner, then choose **Settings**. Open the **Skills** page under Customize:

   ![Settings menu with Skills highlighted under Customize](assets/install-steps/1-settings-skills.png)

3. Click **Add skill**, then **Upload a skill**:

   ![Add skill menu showing Create with Claude, Write skill instructions, and Upload a skill](assets/install-steps/2-add-skill-menu.png)

4. Drag the downloaded `swedish_mentor.skill` file onto the upload box (or click it to browse), then confirm:

   ![Upload skill dialog with a drag-and-drop area](assets/install-steps/3-upload-dialog.png)

5. Start a new chat and ask for a learning plan, for example: “I am A2 and want to improve my speaking before a trip to Sweden.”

Prefer to build the bundle yourself instead of using the pre-packaged file?

```bash
python package_skill.py
python package_skill.py --check
python package_skill.py --install --skills-dir <path-to-skills-folder>
```

The `--check` command validates that the required skill files are present before you use the bundle.

## Demo

A learner says: “I am A2 and want to improve my speaking before a trip to Sweden.” The skill responds with a short plan, a few good video or podcast options, and a clearer next step.

![Skill demo GIF](assets/skill-demo.gif)

## What it does

- Picks a learning path based on level, goal, and skill area.
- Recommends YouTube clips and podcast episodes for listening, reading, writing, and speaking.
- Prioritizes practical channels such as Peter SFI, Lätt Svenska med Oskar, UR Play, and Swedish Shadowing, plus podcasts like Radio Sweden på lätt svenska, Klartext, and Fluent Fiction – Swedish.
- Keeps guidance short, encouraging, and focused on one small step at a time.

## Why it exists

Many learners waste time watching unrelated videos or choosing content that is too hard or too easy. This skill helps them avoid that by offering manageable recommendations and a realistic path forward.

## Live API

The same recommendations are also available as a REST API, deployed on Render:

- Base URL: https://help-with-swedish-api.onrender.com
- Interactive docs: https://help-with-swedish-api.onrender.com/docs

Runs on a free instance, so it spins down after inactivity — the first request after a while can take ~50 seconds. See [api/README.md](api/README.md) for endpoints and local setup.

## Use it

Try prompts such as:

- “I want to improve my Swedish listening for everyday conversations.”
- “I am a beginner and want a simple speaking plan.”
- “Give me good Swedish videos for B1 reading practice.”
- “Recommend a Swedish podcast for my commute.”
- “I want a 2-week plan for learning Swedish for work.”
- “I am A2 and want to improve my vocabulary before moving to Sweden.”
- “I think I’m intermediate at Swedish, but I’m not sure where I really belong.”

A good response usually includes:

- a short level check or suggestion,
- 3–5 video, playlist, or podcast recommendations,
- and one clear next step for the learner.

A strong example looks like this:

> “You seem to be around A2. A good next step is listening practice and short speaking drills. I recommend three short clips and one daily routine.”

## What it helps with

- Choosing a good next step for Swedish learning
- Matching the learner to a level-appropriate path
- Suggesting practical YouTube and podcast resources without overwhelming the learner

## What it does not replace

- A formal language assessment
- A teacher-led placement test
- A guaranteed CEFR score

## Layout

- swedish_mentor/SKILL.md — the skill instructions
- swedish_mentor/references/ — reference files with channel, podcast, and speaking examples
- swedish_mentor.skill — the packaged skill bundle
- universal-prompt.md — plain-text copy-paste version for any AI chat
- assets/install-steps/ — screenshots for the Claude Skill upload walkthrough
- docs/index.html — standalone webpage that calls the live API directly
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
