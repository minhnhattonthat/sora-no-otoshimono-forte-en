# Debug jumps for headless QA (tools/debug/)

No ROM patch: everything is Lua on the DeSmuME QA fork (`jump.lua`, appended to emu.py's driver) plus
`autoplay.lua` (copy of the QA autoplayer: mashes A, Yes on "Go to the next episode?", Retry/Skip at GAME OVER,
backs out of Data Save/help with B). `dbg.py` wraps emu.py with a blank battery save and the right variables.

```
python -X utf8 tools/debug/dbg.py ep4                     # New Game -> Episode 4 part 000 -> autoplay (60k frames)
python -X utf8 tools/debug/dbg.py ep6 --frames 160000 --state-every 20000 --var SKIP=1   # Ep6 to the ending
python -X utf8 tools/debug/dbg.py ending3                 # ending 3 + staff roll + Clear Data save screen
python -X utf8 tools/debug/dbg.py cleardata               # ending 7, saves Clear Data -> work/qa/dbg_cleardata/run_final.dsv
python -X utf8 tools/debug/dbg.py album                   # any screen: album roster titles intimacy training events
                                                          #   actions options help demo, or scene:N
python -X utf8 tools/debug/dbg.py title --sav work/qa/dbg_cleardata/run_final.dsv --route-str "1800 -;6 down;60 -;6 a;200 -;6 down;60 -;6 a;400 -;6 a;150 -;6 a;150 -;6 a;550 -"
                                                          # Tomo-Colle -> Free Communication -> load Clear Data
```
Defaults: `--rom work/run_final.nds` (never build/: DeSmuME streams the ROM), `--out work/qa/dbg_<target>`, shots
every 100 frames. Other arguments pass to emu.py (`--route-str`, `--shot-every`, `--state-every`, `--var X=..`).
Screens opened with a target come up after ~1100 frames; start routes with `1100 -`. A run occasionally hangs at
frame ~40 (no shots after start): rerun. Four parallel runs drop to ~40 fps each.

## jump.lua variables (`--var`)
| var | effect |
|---|---|
| `STORY='ch,num'` | first story script load becomes `Story/ChapterCC/NNN.dat`; chapter byte set too, so Action/Event Select and later parts follow. ch 0-based (Episode 4 = 3); num 0/100/200/300 parts, ch 6 num 1-7 endings (1 Ikaros, 2 Nymph, 3 Astraea, 4 Sohara, 5 Mikako, 6 Sugata, 7 Tomoko), ch 7 num 0 epilogue/tutorial |
| `EVENTS='3,10,1 3,30,1 ..'` | each later story part picked as NEXT is replaced by the next side event `Chara/ChapterCC/AA/BB_000.dat` (= text/en/chara/chCC_AA_BB_000.json); the story resumes after the list |
| `CHOICE='last'` / `'first'` / `n` | force script choices (dbg.py sets `last` for ep/ending: skips "View the tutorial?") |
| `SKIP=1` | GAME OVER menu always takes Skip (even the first time) -> scene counts as given up, story continues |
| `PROC=id` | replace the first switch to the title menu (scene 3) with scene `id`; `PROC_FROM=-1` = next switch of any kind |
| `UNLOCK=1` | at each title-menu switch: all Album items, all communication scenes cleared + Advanced, Tomo-Colle menu, clear count 1, all 28 Titles, all Help topics, 9999 Growth Points, stats level >= 1 |
| `SAVECLEAR=1` | on the Clear Data save screen (scene 15) save to slot 1 |
| `SCENELOG=1` / `SCRIPTLOG=1` | log scene switches / every script id the game builds |
| `POKES='0xADDR=v,..'` (`POKE_AT`, `POKE_EVERY`) | raw byte pokes |

Limits: an `ep` jump keeps New Game stats (LV 1, 0 Growth Points, no intimacy), so the Episode 6 ending is always
Tomoko's (7); use `endingN` for the others. Delusion Select (19) and the staff roll (11) opened with `PROC` show
an empty screen: reach Delusion Communication in-game (Action Select or Free Communication with Clear Data), the
staff roll through `endingN`. UNLOCK's slot data (Titles, Growth Points, Help) only shows on screens opened with
`PROC`: New Game/Continue reload slot data.

## Engine notes found on the way
- Scene (CProc) switch: `0x020538D4(id)` news the next proc; set-next helper `0x020538CC(obj, id)`; current id at
  `0x020E4A58`, current object at `0x020E4A5C`. Ids: 0 boot load, 1 backup init, 2 logos, 3 title menu, 4 ADV
  (story/event script), 5 communication scene (CProcTrial), 6 data save, 8 data load, 9 data load from title
  (Free Communication), 10 system save, 11 staff roll, 12 options, 13 album (CProcGallery), 14 Member Roster (Book),
  15 Clear Data save, 16 chapter-end save, 17 communication results, 18 Action Select, 19 Delusion Select,
  20 Event Select, 21 Tomoki Training, 22 Intimacy, 23 Title List, 24 Help, 25 episode title card, 26 attract demo.
- Script id builder `0x0206964C(obj, buf, num=r2, chapter=r3, [sp] type, [sp+4] chara, [sp+8] sub)`: type 0
  `Chara/Chapter%02d/%02d/%02d_%03d.dat`, 2 `Other/Story/Chapter%02d/%03d.dat`, 3 `Other/Extra/%02d.dat`.
  Called from the script loader `0x020919A0`.
- Global state `G = 0x020DB158` (accessor `0x02031904`); system data (kept across slots, saved at .dsv 0x100):
  `G+0xC4` album flags x28 (`0x02031B94`), `G+0xE0` communication scene state x22 (2 cleared, 4 + Advanced),
  `G+0xF6` Tomo-Colle menu flags x3, `G+0x12C` clear count. Slot data at `G+0x210`: stats `G+0x113C + 4*i`
  (i = 5 is Growth Points), stat levels `G+0x1154` x5, Titles earned `G+0x1668` x28 (`0x02032440`), Help topics
  `G+0x1684` x6, current chapter `G+0x14E9` (0-based, getter `0x02031D6C`).
- Choice commands (ops 2F/D0) exec `0x02089398`; picked index in r1 at `0x020893E0`.
- Communication GAME OVER menu handler `0x0206092C`: r0 at `0x02060970` = 0 Retry, 1 Title, 2 Skip.
- Save file: 64 KB, header "ECHOOF-DEATH" at 0, system data 0x100-0x2A0, slots from 0xA700 (with thumbnails).
