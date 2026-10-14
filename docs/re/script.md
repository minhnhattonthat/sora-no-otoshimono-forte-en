# Story script format (.dat)

Uncompressed. `u32 id, u8 unk, u16 ncmds`, then `ncmds` commands `u8 opcode + args`. The interpreter
(0x02091B6C) parses the whole file into command objects up front: the factory 0x0208FCEC (switch on 0xE6 opcodes,
table at 0x0208FD0C) news one class per opcode and calls vtable[3] = parse(), which reads args with
`read(ctx, dst, n)` at 0x02091A54. Jumps/labels use ids (op 00 = label id, op 02 = conditional), never byte offsets,
so strings can change length freely. `tools/opcodes.py` dumps every opcode's parse() read sizes from arm9.

Variable-size opcodes (hand-read):
- `03` message: `u8 speaker, u8 ?, u8 hasname, [u8 len + name if hasname==1], u8 len + text`. `a9` = same + 1 byte.
- `2f` choices: `u8 n, n bytes, n x (u8 len + text)`; `d0` = `u16` + the same.
- `31`: `u8 n` + n bytes. `73`: `u8, u16, u8 n, n x 4 bytes`.
- `02` condition: 3 bytes + tree: `u8 n; if n: n-1 operator bytes, n x (u8 type: 0 subtree | 1 seven-byte leaf)`.
`tools/script.py` parses all 137 story scripts to exactly `ncmds` with no trailing bytes and rebuilds them byte-identical.

## Text
- Shift-JIS, u8 length prefix (max 255 bytes), no terminator. Longest original string 112 bytes.
- **The renderer walks text in 2-byte units.** `1B xx` control codes are only seen at even offsets, so every
  English segment must be padded to even length (append a space) before a control code.
- `1B 01` newline (x resets, y += 13). Others seen: `1B 1F`, `1B 12`, `1B 11`, `1B 16`, `1B 15`, `1B 14`, `1B 1E`, `1B 20`
  (sizes/effects; handled in the callback 0x0208F070 and preprocessors 0x0208F41C / 0x0208F5A0).
- Box: 3 lines. Japanese lines are up to 18 full-width chars (216 px).

## Renderer / width (engine spike 2026-10-14, build/spike.nds)
- ASCII bytes render from Font1212 (6 px advance each). 36 ASCII chars per line fit (216 px) — verified in-game.
- Typewriter: the unit-copy loop 0x0208EC9C appends each 2-byte unit to a row buffer (0x38 bytes per row at
  obj+0x7BE) and bumps the column (obj+0x9F8 / 0x9F4). Drawing (0x0208EEF4 -> 0x0202BAEC -> NNS DrawString 0x0203A198)
  places each new segment at `x = col * 12 + [obj+0x76C]` (0x0208F3C8 computes the same for the cursor).
  NNS draws a segment proportionally, so the two letters of a unit use real widths, but every unit starts on a
  12 px grid: narrowing advances in the NFTR alone gives "qu ick" gaps. True VWF needs a patch that adds
  (segment width - 12 * units) to [obj+0x76C] after each draw; the newline handler already zeroes it (0x0208F208).
