# RE notes index

- `script.md` — story script .dat format, opcodes, text encoding, renderer.
- `research.md` — prior work, names, game structure (web research 2026-10-14).

## ROM
- `rom/sora-forte.nds`: game code TFLJ, title `SORAOTO-D-S`. MD5 cb616513ee0e8b2c39e3ae0a28b8a924,
  SHA-1 c0a72e86c250ab8b4c8eeee9834a488328e805ee. 128 MiB image, used size 0x7213690, rest 0xFF (~14 MiB free).
- arm9 is BLZ-compressed (ndspy decompresses: `work/arm9.bin`, base 0x02000000, 833,080 bytes). One overlay (ov0, 0x020E4EC0).
- Developer per splash: seventh chord (publisher Kadokawa Shoten). Middleware: CRI (ahx voice), NitroSDK NNS G2d fonts.

## Rebuild
`tools/nds.py` patches the original image in place: a file that fits goes back in its slot, else it is appended
after 0x80 "used size"; FAT, 0x80 and header CRC (0x15E) are updated. No edits = byte-identical (tests/test_identity.py).

## Text sources (survey 2026-10-14)
| Where | What | Size |
|---|---|---|
| `_Data/Script/Other/Story/ChapterNN/*.dat` (39) + `_Data/Script/Chara/ChapterNN/NN/*.dat` (98) | story + character events | 16,686 strings, ~359k JP chars |
| `_Data/Script/Trial/PackScript00-43.dat` | touch-mode lines, different format (not parsed yet) | ~60k chars |
| `_Data/Book/book0[1-5]_*.bin` | gallery/encyclopedia lists (chara, face, voice, bgm, bg) | ~25k chars |
| `_Data/EmblemList/emblem.dat` | titles/emblems + descriptions | ~0.7k |
| `_Data/EventList/EventData/0[0-5].dat` | event/chapter titles | ~0.8k |
| `_Data/AdvTalk/CharaName.dat` | speaker names | small |
| `_Data/Telop/telop_pack.bin` | option-screen help lines | ~0.6k |
| arm9 | save/system error messages | ~0.4k |
| graphics (NCGR/NCBR, many `_LZ`) | title menu, monitor screen, chapter titles, staff roll, help... | survey TODO |

Fonts: `_Data/font/Font1212.NFTR` (dialogue, 1bpp 11x11 cells, 7111 glyphs, full ASCII at 6 px advance),
`Font1010.NFTR` (+ `Font1010ROT90`), same charset.
