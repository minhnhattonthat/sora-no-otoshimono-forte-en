# Sora no Otoshimono Forte: Dreamy Season (NDS) English translation

Skill: translate-retro-game (H:/translation/sora-no-otoshimono-forte-dreamy-season/.claude/skills/translate-retro-game/SKILL.md). Read it before ROM, text or QA work.

## Commands (run from repo root; Python 3.12 with ndspy, capstone, pytest, Pillow)
- Build:    `python -X utf8 tools/build.py` -> build/sora-en.nds (`--identity` = unedited rebuild). Text insertion (tools/insert.py) not written yet.
- Check:    `python -X utf8 tools/check.py` (pytest tests/; the pre-commit hook runs this)
- Smoke:    `python -X utf8 .claude/skills/translate-retro-game/scripts/emu.py build/sora-en.nds --out work/qa/smoke --route-str "1500 -;4 a;300 -;4 a;300 -;4 a;300 -;4 a;900 -;4 a;200 -;4 a;200 -" --shots 3100 --smoke`
  (reaches the first prologue line, Tomoki/Ikaros, at ~f2400; text box crop `--crop 0,312,256,72` in sheet.py)
- Release:  not built yet (xdelta3 on PATH via scoop); never publish without the user.

## Emulator
- DeSmuME QA fork qa-1 in `tools/desmume-qa/DeSmuME.exe` (gitignored; github.com/minhnhattonthat/desmume/releases). emu.py finds it automatically. Headless, ~4 s per 900 frames.
- Lua helpers: `tools/lua/who_reads.lua` (pc/lr of reads in a range), `tools/lua/drawstr.lua` (DrawString calls).

## Paths
- Original ROM: `rom/sora-forte.nds` (gitignored; hashes in docs/re/README.md). Scratch/savestates: `work/`. Decompressed arm9: `work/arm9.bin` (regenerate with ndspy, see docs/re/README.md).
- Code: `tools/` — romfs.py (NitroFS name->id), nds.py (in-place file replace), script.py (script codec), opcodes.py (opcode arg sizes from arm9), build.py.
- RE notes: `docs/re/README.md` (index, text sources), `docs/re/script.md`, `docs/re/research.md`.

## Rulings
- Edit source files only with the file-edit tool. Text strings: pad each segment to even byte length before a `1B xx` control code (renderer reads 2-byte units).
- Names: Funimation anime spellings (manga never licensed in English). Other rulings pending user answers.

## Status
- Done: recon, script codec (137 files byte-identical), identity build, engine spike (ASCII renders, 36 chars x 3 lines at 6 px).
- Next: decide VWF (patch at 0x0208EEF4 draw loop, see script.md), Trial/PackScript format, extract to text/, marker build + width gate.
