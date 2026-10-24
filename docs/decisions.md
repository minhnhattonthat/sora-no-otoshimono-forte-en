# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

Rows D1-D7 were collected from earlier notes when the repo moved to the template; the options offered then were not
recorded.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-14 | Honorifics and name order | keep (-san), drop; JP or Western order | Kept, hyphenated; given name first (Tomoki Sakurai). |
| D2 | 2026-10-14 | Romanization source for names | official English release, Hepburn | Funimation anime spellings (no English manga); Hepburn without long-vowel marks otherwise. |
| D3 | 2026-10-14 | Credits | stay Japanese, translate | English, staff roll included. |
| D4 | 2026-10-14 | Abbreviations | engine work first (default), abbreviate | Full names and terms; VWF box, ~40-44 chars per line, 3 lines. |
| D5 | 2026-10-15 | Graphics text left in Japanese | none (default), list | None; logos redrawn after the official English logo (first kept Japanese, then replaced). |
| D6 | 2026-10-14 | Specs and plans | need approval, pre-approved | Pre-approved; whole game in one go. |
| D7 | 2026-10-15 | Play-testing | user plays, automated | Automated QA only: build debug jumps to reach unplayed content; the user won't play-test. |
| D8 | 2026-10-24 | Repo layout | as is, fan-translation-template | Template docs/config; text/, gfx/ and tools/ stay where they are (sibling repos did the same). |
