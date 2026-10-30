# Sora no Otoshimono Forte: Dreamy Season English translation

Unofficial English fan translation of **Sora no Otoshimono Forte: Dreamy Season** (Heaven's Lost Property Forte:
Dreamy Season; Nintendo DS, Kadokawa Shoten / seventh chord): the source text and tools that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game (game code TFLJ).

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Dialogue / story (story, character events, touch mode, choices, speaker names) | Translated |
| Menus, help, tutorials, event titles, save screens, system messages | Translated |
| Title logo and graphics with text | Translated (logo redrawn after the official English logo) |
| Staff roll | Translated (some name readings are guesses) |
| Voiced lines | Left in Japanese (voice acting unchanged) |

Names follow Funimation's anime release; honorifics are kept. Tested in DeSmuME only (not on hardware).

Known issues: 21 staff-roll name readings are unverified (`docs/re/graphics.md`), and where Japanese credits crossed
character art the cleaned-up area is slightly blurred; corrections welcome.

## What's here

| Path | What it is |
|---|---|
| `text/` | Every text block: extracted Japanese (`text/ja`) and English (`text/en`). Translation fixes go here. |
| `gfx/edits/` | Graphics specs: redrawn menus, titles, help screens, staff roll, logo. |
| `glossary.md` | Binding names, terms and style rules. |
| `tools/` | Python build chain: extract, insert, VWF, graphics, release; `tools/debug/` headless QA jumps. |
| `tests/` | pytest suite (needs the ROM). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |

## Build your own patched ROM

Needs Python 3.12+ with `ndspy capstone keystone Pillow pytest`, Windows (graphics specs use Windows fonts) and your
own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/sora-no-otoshimono-forte-en
cd sora-no-otoshimono-forte-en
# copy your dump to: rom/sora-forte.nds
#   (134,217,728 bytes, SHA-1 c0a72e86c250ab8b4c8eeee9834a488328e805ee; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/sora-en.nds
python -X utf8 tools/check.py                          # tests
python -X utf8 tools/release.py v1.0                   # xdelta patch + README + zip
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `text/ja` is the rights holders' and is included
only so the translation can be checked against it. Sora no Otoshimono is (c) Suu Minazuki / Kadokawa; the game is by
seventh chord. This project is not affiliated with them. Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
