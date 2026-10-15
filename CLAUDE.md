# Sora no Otoshimono Forte: Dreamy Season (NDS) English translation

Skill: translate-retro-game (H:/translation/sora-no-otoshimono-forte-dreamy-season/.claude/skills/translate-retro-game/SKILL.md). Read it before ROM, text or QA work.

## Commands (run from repo root; Python 3.12 with ndspy, capstone, keystone, pytest, Pillow)
- Build:    `python -X utf8 tools/build.py [--out X.nds]` -> build/sora-en.nds (`--identity` = unedited rebuild; `MARKER=1` = id markers)
- Check:    `python -X utf8 tools/check.py` (pytest tests/; the pre-commit hook runs this)
- Smoke:    copy the build first (see Emulator), then `python -X utf8 .claude/skills/translate-retro-game/scripts/emu.py work/run.nds --out work/qa/smoke --route-str "1500 -;4 a;300 -" --mash 30 --frames 3000 --smoke`
- Text batches: `tools/batches.py split|check|merge|fit|status`; global term swap: `tools/retext.py "old=>new"`; review samples: `tools/pairs.py`.
- Graphics: specs in gfx/edits/ (gfx/README.md), `tools/gfxedit.py orig|preview SPEC`; inventory docs/re/graphics.md.
- Release:  `python -X utf8 tools/release.py vX.Y` -> release/*.zip (xdelta3 via scoop); never publish without the user.

## Emulator
- DeSmuME QA fork qa-1 in `tools/desmume-qa/DeSmuME.exe` (gitignored). emu.py finds it. Headless, ~4 s per 900 frames.
- **Run emulator QA on a copy of the ROM** (`cp build/sora-en.nds work/run_X.nds`): DeSmuME streams the ROM from disk,
  so rebuilding during a run corrupts it (looked like a hang with garbage graphics).
- First prologue line at ~f2400 (A at f1500 on title). Long A-mash runs with `--state-every 10000` give savestates.
- Lua helpers: tools/lua/ (who_reads, drawstr, rowdraw, choice_log).

## Paths
- Original ROM: `rom/sora-forte.nds` (gitignored; hashes in docs/re/README.md). Scratch: `work/`.
- Text: text/ja (extracted), text/en/{story,chara,trial}/*.json (id -> English), text/en/names.json (speaker plates),
  text/en/misc.json (event titles, emblems, gallery lists, option help), text/en/arm9.json (system messages).
- Code: tools/ — nds.py (in-place ROM files), script.py (script codec), extract/insert/textfmt (text), vwf.py (VWF hook +
  font), misctext/lpstr (small data files), arm9text, gfx/gfxedit/lz11 (graphics), opcodes.py (RE).
- RE notes: docs/re/README.md, script.md, research.md, graphics.md.

## Rulings
- Honorifics kept, given name first, Funimation spellings; credits English; whole game; plans pre-approved.
- Text: pad to even bytes before control codes (insert does it); `{1F}{xx}` SFX lines re-centred automatically;
  overflow > 3 lines spills into a second box; ☆ ♪ ♥ drawn from ASCII slots ^ ` |.
- Speaker plates <= 72 px. Choices <= 200 px.

## Status (2026-10-15)
- Done: engine (VWF, overflow boxes), all 20,046 script strings translated + merged, names, misc files, arm9 strings,
  graphics specs for every screen found (incl. staff roll, EventMain tutorial, NormalMain delusion banner), sampled review.
- Fixed from QA: Trial pack block lengths (scenes stuck at 00:00), quote glyphs, Trial lines kept to 2 rows.
- Leftover-Japanese scan (code + script/data files): clean. Title logo kept Japanese. 21 staff-name readings unverified
  (docs/re/graphics.md).
- QA routes: cold boot "1500 -;4 a;300 -" --mash 20 reaches Event Select ~f26000; A opens "Go to the next episode?"
  (default No: left, A). Trial tutorial menu needs d-pad, not touch. Pause > Skip passes a Trial scene.
- Graphics specs use Windows fonts (arialbd, arialnb, comicz, segoeuib, ...): build on Windows.
- QA played to the start of Ep4 (autoplay Lua work/qa/autoplay.lua: A-mash, Yes on next episode, Retry/Skip at
  GAME OVER; Skip appears from the 2nd GAME OVER). Dark bands in Trial scenes are original behaviour.
- Debug jumps: `python -X utf8 tools/debug/dbg.py ep4|events5|ending3|training|album|...` (docs/re/debug.md).
  Covered Ep1-6, all side events, 7 endings + staff roll, Clear Data, all unlock screens.
- English logo (MainTitle/logo_en.py) on title, episode logo, staff roll, options.
- v1.0 package built locally (release/, patched CRC32 1F211647); not published.
- Next: user decision on publishing.
