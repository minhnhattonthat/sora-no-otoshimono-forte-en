# Sora no Otoshimono Forte: Dreamy Season (NDS) English translation

Skill: translate-retro-game (Claude Code: plugin, enabled in .claude/settings.json; other agents: `<SKILL_DIR>/SKILL.md`; `$SKILL` = the directory holding its SKILL.md, default `~/.claude/plugins/marketplaces/retro-translation/skills/translate-retro-game`). Read it before ROM, text or QA work.

## Commands (run from repo root; Python 3.12 with ndspy, capstone, keystone, pytest, Pillow)
- Build:    `python -X utf8 tools/build.py [--out X.nds]` -> build/sora-en.nds (checks the dump against `rom.sha1` first; `--identity` = unedited rebuild; `MARKER=1` = id markers)
- Check:    `python -X utf8 tools/check.py` (pytest tests/; the pre-commit hook runs this)
- Smoke:    copy the build first (see Gotchas), then `python -X utf8 $SKILL/scripts/emu.py work/run.nds --out work/qa/smoke --route-str "1500 -;4 a;300 -" --mash 30 --frames 3000 --smoke`
- Warp:     `python -X utf8 tools/debug/dbg.py ep4|events5|ending3|training|album|...` (docs/re/debug.md; never ask the user to play to a scene)
- Text batches: `tools/batches.py split|check|merge|fit|status`; global term swap: `tools/retext.py "old=>new"`; review samples: `tools/pairs.py`.
- Graphics: specs in gfx/edits/ (gfx/README.md), `tools/gfxedit.py orig|preview SPEC`; inventory docs/re/graphics.md.
- Release:  `python -X utf8 tools/release.py vX.Y` -> release/*.zip (xdelta3 via scoop); never publish without the user.
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)

## Paths
- Original ROM: `rom/sora-forte.nds` (gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`; MD5 in docs/re/README.md). Emulator: DeSmuME QA fork qa-1 in `tools/desmume-qa/DeSmuME.exe` (gitignored; emu.py finds it; headless, ~4 s per 900 frames). Savestates: `work/states/`. Scratch: `work/`.
- Text: text/ja (extracted), text/en/{story,chara,trial}/*.json (id -> English), text/en/names.json (speaker plates),
  text/en/misc.json (event titles, emblems, gallery lists, option help), text/en/arm9.json (system messages).
- Code: tools/ — nds.py (in-place ROM files), script.py (script codec), extract/insert/textfmt (text), vwf.py (VWF hook +
  font), misctext/lpstr (small data files), arm9text, gfx/gfxedit/lz11 (graphics), opcodes.py (RE). Lua helpers: tools/lua/ (who_reads, drawstr, rowdraw, choice_log).
- Glossary: `glossary.md`. RE notes index: `docs/re/README.md` (script.md, research.md, graphics.md, debug.md). Fonts and their licences: `docs/fonts.md`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Text: pad to even bytes before control codes (insert does it); `{1F}{xx}` SFX lines re-centred automatically;
  overflow > 3 lines spills into a second box; ☆ ♪ ♥ drawn from ASCII slots ^ ` |.
- Speaker plates <= 72 px. Choices <= 200 px. Trial lines <= 2 rows.

## Gotchas
- **Run emulator QA on a copy of the ROM** (`cp build/sora-en.nds work/run_X.nds`): DeSmuME streams the ROM from disk,
  so rebuilding during a run corrupts it (looked like a hang with garbage graphics).
- First prologue line at ~f2400 (A at f1500 on title). Long A-mash runs with `--state-every 10000` give savestates.
- Cold boot "1500 -;4 a;300 -" --mash 20 reaches Event Select ~f26000; A opens "Go to the next episode?"
  (default No: left, A). Trial tutorial menu needs d-pad, not touch. Pause > Skip passes a Trial scene.
  Autoplay Lua: tools/lua/autoplay.lua (A-mash, Yes on next episode, Retry/Skip at GAME OVER; Skip appears from the 2nd GAME OVER).
- Graphics specs use Windows fonts (arialbd, arialnb, comicz, segoeuib, ...; docs/fonts.md): build on Windows.
- Dark bands in Trial scenes are original behaviour.
- tools/ subdirectories are gitignored (third-party downloads) except tools/debug/, tools/lua/, tools/routes/.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
