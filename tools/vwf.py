"""Variable-width English in the dialogue box. See docs/re/script.md "Renderer / width".

1. Font1212.NFTR: ASCII glyphs get left=0, advance = ink width + 1 (space: SPACE_ADV).
2. arm9: the typewriter places every 2-byte unit on a 12 px grid (x = col*12 + [obj+0x76C]). After the row-draw
   loop (0x0208F064) a hook adds sum(adv(b1) + adv(b2) - 12) over the last row's ASCII units to [obj+0x76C], so
   the next unit starts where the text really ends. The hook lives in the ITCM autoload section (grown), and the
   ITCM arena start literal (0x02005D4C) moves past it.
"""
import struct

import ndspy.code
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM

HOOK_AT = 0x0208F064          # 'add sp, sp, #0xc' before 'pop {r4-fp, pc}' of the horizontal draw routine
ITCM_ARENA_LIT = 0x02005D4C   # literal 0x01FF8540 returned by OS_GetInitArenaLo(ITCM)
SPACE_ADV = 3

HOOK = """
    ldrb r0, [r10, #0x9ee]
    sub r0, r0, #1
    mov r1, #0x38
    add r2, r10, #0x700
    add r2, r2, #0xbe
    mla r2, r0, r1, r2
    ldrb r3, [r10, #0x9ef]
    ldr r0, [r10, #0x76c]
    add r12, pc, #TABLE_REL
    mov r1, #0
loop:
    cmp r1, r3
    bhs done
    ldrb r4, [r2, r1]
    add r1, r1, #1
    ldrb r5, [r2, r1]
    add r1, r1, #1
    cmp r4, #0x20
    blo loop
    cmp r4, #0x80
    bhs loop
    ldrb r4, [r12, r4]
    ldrb r5, [r12, r5]
    add r0, r0, r4
    add r0, r0, r5
    sub r0, r0, #12
    b loop
done:
    str r0, [r10, #0x76c]
    add sp, sp, #0xc
    pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
"""


def hook_src(table_rel):
    return HOOK.replace('TABLE_REL', str(table_rel))


def font_widths(nftr):
    """Return (patched NFTR bytes, 256-byte advance table) with proportional ASCII."""
    f = bytearray(nftr)
    hdwc = struct.unpack_from('<I', f, 0x10 + 0x14)[0]
    first, last = struct.unpack_from('<HH', f, hdwc)
    assert first == 0 and last > 0x5e
    table = bytearray([6] * 256)  # bytes >= 0x80 never reach the table; 6 keeps a stray one harmless
    for c in range(0x20):
        table[c] = 0
    plgc = struct.unpack_from('<I', f, 0x10 + 0x10)[0]
    tsz = struct.unpack_from('<H', f, plgc + 2)[0]
    for c in range(0x20, 0x7f):
        g = c - 0x20  # ASCII glyphs 0..94 map to 0x20..0x7e (CMAP direct block)
        o = hdwc + 8 + 3 * g
        if c in SYMBOLS:  # copy a full-width symbol into this unused ASCII slot (single byte = no padding space)
            src = glyph_index(f, SYMBOLS[c])
            f[plgc + 8 + g * tsz:plgc + 8 + (g + 1) * tsz] = f[plgc + 8 + src * tsz:plgc + 8 + (src + 1) * tsz]
            ink = f[hdwc + 8 + 3 * src + 1]
            f[o:o + 3] = bytes([1, ink, ink + 2])
            table[c] = ink + 2
            continue
        if c in GLYPHS:  # the font's ' and " are slashes that read as accents
            rows = GLYPHS[c]
            bits = ''.join(r.replace('#', '1').replace('.', '0').ljust(11, '0') for r in rows).ljust(tsz * 8, '0')
            f[plgc + 8 + g * tsz:plgc + 8 + (g + 1) * tsz] = int(bits, 2).to_bytes(tsz, 'big')
            f[o + 1] = max(len(r.rstrip('.')) for r in rows)
        ink = f[o + 1]
        adv = SPACE_ADV if c == 0x20 else ink + 1
        f[o], f[o + 2] = 0, adv
        table[c] = adv
    return bytes(f), bytes(table)


# ASCII byte -> Shift-JIS code of the symbol drawn there: ^ = ☆, ` = ♪, | = heart (the font's Ω glyph)
SYMBOLS = {0x5E: 0x8199, 0x60: 0x81F4, 0x7C: 0x83B6}  # textfmt.SYMBOLS maps the characters to these bytes

# 11x11 1 bpp cells, top rows only; quotes shaped like the font's comma, < > as chevrons (the font's read as parens)
GLYPHS = {0x27: ['##', '##', '.#', '#.'], 0x22: ['##.##', '##.##', '.#..#', '#..#.'],
          0x3E: ['', '', '', '#...', '.##.', '...#', '.##.', '#...'],
          0x3C: ['', '', '', '...#', '.##.', '#...', '.##.', '...#']}


def glyph_index(f, code):
    pamc = struct.unpack_from('<I', f, 0x10 + 0x18)[0]
    p = pamc
    while p:
        lo, hi, typ, nxt = struct.unpack_from('<HHHxxI', f, p)
        body = p + 12
        if lo <= code <= hi:
            if typ == 0:
                return struct.unpack_from('<H', f, body)[0] + code - lo
            if typ == 1:
                return struct.unpack_from('<H', f, body + 2 * (code - lo))[0]
        if typ == 2:
            for i in range(struct.unpack_from('<H', f, body)[0]):
                c, g = struct.unpack_from('<HH', f, body + 2 + 4 * i)
                if c == code:
                    return g
        p = nxt
    raise KeyError(hex(code))


def assemble(code, addr):
    enc, _ = Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(code, addr)
    return bytes(enc)


def patch_arm9(arm9, ram, settings_ptr, table, text_patch=None):
    """arm9: compressed arm9 bytes from the ROM. text_patch(main_bytes) -> bytes edits data in place (strings).
    Returns new compressed arm9."""
    code = ndspy.code.MainCodeFile(arm9, ram, settings_ptr)
    main = code.sections[0]
    itcm = [s for s in code.sections if s.ramAddress == 0x01FF8000][0]
    cave = itcm.ramAddress + len(itcm.data)
    assert cave % 4 == 0
    probe = assemble(hook_src(0), cave)
    table_at = cave + len(probe)
    hook = assemble(hook_src(table_at - (cave + 8 * 4 + 8)), cave)  # 'add r12, pc' is instr #8
    assert len(hook) == len(probe)
    blob = hook + table
    itcm.data = bytes(itcm.data) + blob + b'\0' * (-len(blob) % 32)
    new_end = itcm.ramAddress + len(itcm.data)

    m = bytearray(text_patch(bytes(main.data)) if text_patch else main.data)
    lit = ITCM_ARENA_LIT - main.ramAddress
    assert struct.unpack_from('<I', m, lit)[0] == 0x01FF8540
    struct.pack_into('<I', m, lit, new_end)
    at = HOOK_AT - main.ramAddress
    assert m[at:at + 4] == bytes.fromhex('0cd08de2')  # add sp, sp, #0xc
    m[at:at + 4] = assemble(f'b #{cave:#x}', HOOK_AT)
    main.data = bytes(m)
    return code.save(compress=True)


def selftest():
    h = assemble(hook_src(0), 0x01FF8540)
    # instr #8 must be the pc-relative add the table offset is computed for
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    ins = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(h, 0x01FF8540))
    assert ins[8].mnemonic == 'add' and 'pc' in ins[8].op_str, ins[8]
    assert all(i.mnemonic != 'bl' for i in ins)
    return len(h)


if __name__ == '__main__':
    print('hook bytes', selftest())
