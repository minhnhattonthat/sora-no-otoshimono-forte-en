# Sora no Otoshimono Forte: Dreamy Season - English translation (Nintendo DS)

Unofficial fan translation of *Sora no Otoshimono Forte: Dreamy Season* (Heaven's Lost Property Forte: Dreamy Season),
with the tools that built it. **No ROM is included.** You need your own dump of the Japanese game (game code TFLJ).

## Play it

Download the zip from the [Releases](../../releases) page and apply the `.xdelta` patch to your ROM with xdelta3
(or Delta Patcher / xdelta UI). Expected original ROM: 134,217,728 bytes, MD5 `cb616513ee0e8b2c39e3ae0a28b8a924`,
SHA-1 `c0a72e86c250ab8b4c8eeee9834a488328e805ee`. Details are in the release README.

## What's translated

All story, character-event and touch-mode dialogue, choices, speaker names, menus, help, tutorials, event titles,
save screens, staff roll, system messages and the logo. Names follow Funimation's anime release; honorifics are kept.
Voices stay Japanese. Tested in DeSmuME only (not on hardware).

## Build it yourself

Python 3.12 with `ndspy capstone keystone Pillow pytest`; Windows (graphics specs use Windows fonts).
Put the original ROM at `rom/sora-forte.nds`, then:

```
python -X utf8 tools/build.py        # -> build/sora-en.nds
python -X utf8 tools/check.py        # tests
python -X utf8 tools/release.py v1.0 # xdelta patch + README + zip
```

Layout: `text/en` translations (`text/ja` is the extracted source), `gfx/edits` graphics specs, `tools/` build and
reverse-engineering tools, `tools/debug` headless QA jumps, `docs/re` format and debug notes, `glossary.md` terms.

Staff-roll name readings are partly guesses (`docs/re/graphics.md`); corrections welcome.

Translation and hacking were produced with AI assistance (Claude). Thanks to Suu Minazuki, Kadokawa and seventh chord
for the original game.

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)
