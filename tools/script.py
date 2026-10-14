"""Script (.dat) codec. Format in docs/re/script.md.

File: u32 id, u8 unk, u16 ncmds, then ncmds commands: u8 opcode + args (sizes from tools/opcodes.py).
Strings are u8 length + Shift-JIS bytes (no terminator); 1B 01 inside a string is a line break.
"""
import struct

# opcode -> list of fixed arg sizes (bytes), from tools/opcodes.py (static analysis of each parse())
FIXED = {
    0x00: [1], 0x01: [1], 0x04: [4], 0x05: [], 0x06: [], 0x07: [1, 1], 0x08: [1, 1], 0x09: [1, 2], 0x0a: [1, 2],
    0x0b: [1, 1, 1, 1], 0x0c: [1, 1, 2], 0x0d: [1, 2, 2], 0x0e: [1, 2, 2], 0x0f: [1, 1, 1, 1, 2], 0x10: [1],
    0x13: [1], 0x14: [1], 0x15: [1], 0x16: [1], 0x17: [1], 0x18: [1, 2], 0x19: [], 0x1b: [], 0x1c: [1, 1],
    0x1d: [2, 1], 0x24: [1], 0x25: [1], 0x26: [1], 0x27: [1, 1], 0x28: [1, 1, 1], 0x29: [], 0x2a: [1],
    0x2b: [], 0x2c: [2], 0x2d: [2], 0x2e: [2, 1], 0x32: [], 0x33: [1], 0x35: [2], 0x36: [2, 2], 0x39: [],
    0x3a: [1, 1], 0x3b: [1, 1, 1, 1], 0x3c: [1, 1, 2], 0x3d: [1, 1, 1, 1, 2], 0x3e: [1], 0x3f: [1], 0x41: [],
    0x42: [1], 0x43: [1], 0x44: [1, 1], 0x45: [], 0x46: [], 0x47: [4, 4], 0x48: [1, 1, 1], 0x49: [1, 1, 2, 1],
    0x4a: [1], 0x4b: [1], 0x4c: [1, 4, 4], 0x4d: [1], 0x4e: [1, 2], 0x4f: [1, 1], 0x50: [1, 1, 2], 0x51: [2],
    0x52: [], 0x5a: [1, 1], 0x5b: [1, 1], 0x5c: [1, 1], 0x5d: [2], 0x5f: [1, 1, 2, 1], 0x64: [1], 0x66: [],
    0x67: [2], 0x69: [], 0x6a: [], 0x6e: [1, 1, 1, 1], 0x72: [2], 0x82: [1], 0x84: [1, 1], 0x85: [1, 1, 1],
    0x86: [1, 1, 1], 0x87: [1, 2], 0x89: [2], 0x8b: [1], 0x8f: [], 0x91: [2], 0x93: [1, 1, 2, 2], 0xa2: [1],
    0xa3: [1, 1, 2, 2, 2], 0xa4: [1, 2], 0xa5: [1], 0xa7: [], 0xa8: [1], 0xaa: [4], 0xae: [2, 1, 1, 1],
    0xb0: [1, 2], 0xb2: [1, 2, 2], 0xb4: [1], 0xb5: [1], 0xbf: [1, 1], 0xc0: [1, 1], 0xc3: [1], 0xc8: [],
    0xc9: [1, 1, 1], 0xca: [1, 1, 1], 0xcb: [1], 0xcd: [], 0xcf: [1], 0xd1: [1], 0xd2: [2, 2], 0xd3: [2, 2],
    0xd4: [2], 0xd5: [2], 0xd6: [], 0xd7: [], 0xd8: [2, 2, 2], 0xd9: [], 0xda: [1, 1], 0xdb: [1, 1, 1, 2, 2, 2, 2],
    0xdc: [1], 0xdd: [1, 1], 0xde: [1, 1], 0xdf: [1, 1, 1], 0xe0: [1], 0xe1: [1, 1, 2, 2, 1], 0xe2: [1, 4],
    0xe3: [1], 0xe4: [1], 0xe5: [],
}
# Variable layouts. Items: int = raw bytes, 'S' = u8-length string, 'N' = u8 n then n raw bytes,
# 'T' = text (u8 speaker, u8, u8 hasname, [S name], S text), 'C' = choices (u8 n, n raw bytes, n S).
VAR = {
    0x03: ['T'],
    0xa9: ['T', 1],
    0x2f: ['C'],
    0xd0: [2, 'C'],
    0x31: ['N'],
    0x02: [3, 'E'],
    0x73: [1, 2, 'Q'],
}
# 'E' = condition tree (0x208A554): u8 n; if n: n-1 operator bytes, then n x (u8 type: 0 = subtree, 1 = 7-byte leaf)
# 'Q' = u8 n, then n x 4 bytes (0x208CF48)


class Cmd:
    __slots__ = ('op', 'parts')  # parts: list of bytes (raw) or str-marked tuples ('s', bytes)

    def __init__(self, op, parts):
        self.op, self.parts = op, parts

    def strings(self):
        return [p[1] for p in self.parts if isinstance(p, tuple)]

    def encode(self):
        out = bytearray([self.op])
        for p in self.parts:
            if isinstance(p, tuple):
                if len(p[1]) > 255:
                    raise ValueError(f'string over 255 bytes in op {self.op:02x}')
                out += bytes([len(p[1])]) + p[1]
            else:
                out += p
        return bytes(out)


def parse(data):
    sid, unk, n = struct.unpack_from('<IBH', data, 0)
    pos, cmds = 7, []

    def raw(k):
        nonlocal pos
        b = data[pos:pos + k]
        if len(b) != k:
            raise ValueError('ran past end of file')
        pos += k
        return b

    def s():
        return ('s', raw(raw(1)[0]))

    def tree():
        k = raw(1)
        out = [k]
        if k[0]:
            out.append(raw(k[0] - 1))
            for _ in range(k[0]):
                t = raw(1)
                out.append(t)
                if t[0] == 0:
                    out += tree()
                elif t[0] == 1:
                    out.append(raw(7))
                else:
                    raise ValueError(f'bad condition node type {t[0]} at {pos - 1:#x}')
        return out

    for _ in range(n):
        start = pos
        op = data[pos]
        pos += 1
        parts = []
        if op in FIXED:
            parts = [raw(sum(FIXED[op]))] if FIXED[op] else []
        elif op in VAR:
            for it in VAR[op]:
                if isinstance(it, int):
                    parts.append(raw(it))
                elif it == 'S':
                    parts.append(s())
                elif it == 'N':
                    k = raw(1)
                    parts += [k, raw(k[0])]
                elif it == 'T':
                    h = raw(3)
                    parts.append(h)
                    if h[2] == 1:
                        parts.append(s())
                    parts.append(s())
                elif it == 'E':
                    parts += tree()
                elif it == 'Q':
                    k = raw(1)
                    parts += [k, raw(4 * k[0])]
                elif it == 'C':
                    k = raw(1)
                    parts += [k, raw(k[0])] + [s() for _ in range(k[0])]
        else:
            raise ValueError(f'unknown opcode {op:02x} at {start:#x}')
        cmds.append(Cmd(op, parts))
    return sid, unk, cmds, data[pos:]


def build(sid, unk, cmds, tail=b''):
    return struct.pack('<IBH', sid, unk, len(cmds)) + b''.join(c.encode() for c in cmds) + tail
