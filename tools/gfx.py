"""Nitro 2D graphics: NCLR palettes, NCGR/NCBR character data, NSCR screens -> PIL images, and back.

python -X utf8 tools/gfx.py dump FOLDER [FOLDER..]   -> work/gfx/<folder>/<name>.png for every NCGR/NCBR
Files ending _LZ are LZ10-compressed. NCBR stores pixels linearly (a bitmap), NCGR in 8x8 tiles.
"""
import os
import struct
import sys

import ndspy.lz10
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))


def unlz(d):
    if d[:1] == b'\x10':
        return bytes(ndspy.lz10.decompress(d))
    if d[:1] == b'\x11':
        import lz11
        return lz11.decompress(bytes(d))
    return bytes(d)


def section(d, magic):
    pos = struct.unpack_from('<H', d, 0xC)[0]
    while pos + 8 <= len(d):
        m, size = d[pos:pos + 4], struct.unpack_from('<I', d, pos + 4)[0]
        if m == magic:
            return pos
        if size == 0:
            break
        pos += size
    raise KeyError(magic)


def container(d):
    """Some files carry a 4-byte prefix (u32) before the Nitro header; return the bytes from the magic on."""
    return d[4:] if d[4:8] in (b'RGCN', b'RLCN', b'RCSN', b'RECN') and d[:4] not in (b'RGCN', b'RLCN') else d


def palette(nclr):
    nclr = container(unlz(nclr))
    s = section(nclr, b'TTLP')
    depth, _, size, off = struct.unpack_from('<IIII', nclr, s + 8)
    data = nclr[s + 8 + off:s + 8 + off + size]
    cols = []
    for i in range(0, len(data) - 1, 2):
        v = struct.unpack_from('<H', data, i)[0]
        cols.append(((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31))
    return cols, (4 if depth == 3 else 8)


class Char:
    """Character data: .pixels = list of palette indices, laid out as a w x h pixel image."""

    def __init__(self, raw):
        self.prefix = unlz(raw)[:4]
        self.raw = raw = container(unlz(raw))
        self.sec = s = section(raw, b'RAHC')
        self.th, self.tw, depth, _, self.linear, self.size, self.off = struct.unpack_from('<HHIIIII', raw, s + 8)
        self.bpp = 4 if depth == 3 else 8
        self.data = raw[s + 8 + self.off:s + 8 + self.off + self.size]
        n = len(self.data) * 8 // self.bpp
        idx = []
        for b in self.data:
            idx += [b & 15, b >> 4] if self.bpp == 4 else [b]
        self.idx = idx[:n]
        if self.tw == 0xFFFF or self.th == 0xFFFF:
            self.tw = 32 if self.linear else 32
            self.th = -(-n // (self.tw * 64))
        self.w, self.h = self.tw * 8, self.th * 8

    def tile(self, t):
        """64 indices of 8x8 tile t (tiled data)."""
        return self.idx[t * 64:(t + 1) * 64]

    def encode(self, idx, orig):
        """Rebuild the file from a full index list (may be longer than before: tiles appended), compressed like
        `orig` (LZ10 / LZ11 / none) and with the same 4-byte prefix if it had one."""
        if self.bpp == 4:
            data = bytes(idx[i] | idx[i + 1] << 4 for i in range(0, len(idx), 2))
        else:
            data = bytes(idx)
        s, raw = self.sec, bytearray(self.raw)
        start = s + 8 + self.off
        grow = len(data) - self.size
        raw[start:start + self.size] = data
        if grow:
            struct.pack_into('<I', raw, s + 4, struct.unpack_from('<I', raw, s + 4)[0] + grow)  # section size
            struct.pack_into('<I', raw, s + 8 + 16, len(data))  # data size
            struct.pack_into('<I', raw, 8, struct.unpack_from('<I', raw, 8)[0] + grow)  # file size
            th, tw = struct.unpack_from('<HH', raw, s + 8)
            if th != 0xFFFF and tw not in (0, 0xFFFF):
                struct.pack_into('<H', raw, s + 8, -(-len(idx) // (tw * 64)))
        out = bytes(raw)
        u = unlz(orig)
        if u[4:8] in (b'RGCN', b'RBCN') and u[:4] not in (b'RGCN', b'RBCN'):
            out = u[:4] + out
        if orig[:1] == b'\x10':
            return bytes(ndspy.lz10.compress(out))
        if orig[:1] == b'\x11':
            import lz11
            return lz11.compress(out)
        return out

    def image(self, pal, pal_off=0):
        img = Image.new('RGB', (self.w, self.h))
        px = img.load()
        get = (lambda i: pal[pal_off + i] if pal_off + i < len(pal) else (255, 0, 255))
        if self.linear:
            for i, v in enumerate(self.idx[:self.w * self.h]):
                px[i % self.w, i // self.w] = get(v)
        else:
            for t in range(min(self.tw * self.th, len(self.idx) // 64)):
                tx, ty = t % self.tw * 8, t // self.tw * 8
                for i, v in enumerate(self.tile(t)):
                    px[tx + i % 8, ty + i // 8] = get(v)
        return img


def screen(nscr, char, pal):
    s = section(nscr, b'NRCS')
    w, h, _, size = struct.unpack_from('<HHII', nscr, s + 8)
    ents = struct.unpack_from('<%dH' % (size // 2), nscr, s + 0x14)
    img = Image.new('RGB', (w, h))
    px = img.load()
    cols = w // 8
    for k, e in enumerate(ents):
        t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        tile = char.tile(t)
        if not tile:
            continue
        bx, by = k % cols * 8, k // cols * 8
        if by >= h:
            break
        for i, v in enumerate(tile):
            x, y = i % 8, i // 8
            if hf:
                x = 7 - x
            if vf:
                y = 7 - y
            off = p * 16 if char.bpp == 4 else 0
            c = pal[off + v] if off + v < len(pal) else (255, 0, 255)
            px[bx + x, by + y] = c
    return img


def dump(folders):
    import romfs
    rom, ids = romfs.load()
    for folder in folders:
        out = os.path.join('work', 'gfx', folder.replace('/', '_'))
        os.makedirs(out, exist_ok=True)
        names = {p[len('_Data/' + folder) + 1:]: f for p, f in ids.items() if p.startswith('_Data/' + folder + '/')}
        for n in sorted(names):
            if not n.endswith(('.NCGR', '.NCBR')) or '/' in n:
                continue
            base = n[:-5].replace('_LZ', '')
            try:
                ch = Char(bytes(rom.files[names[n]]))
                nclr = names.get(base + '.NCLR')
                pal = palette(bytes(rom.files[nclr]))[0] if nclr else [(i * 16 % 256,) * 3 for i in range(256)]
                nscr = names.get(base + '.NSCR')
                img = screen(bytes(rom.files[nscr]), ch, pal) if nscr and not ch.linear else ch.image(pal)
                img.save(os.path.join(out, base + '.png'))
            except Exception as e:
                print('skip', folder, n, e)
        print(folder, 'done')


if __name__ == '__main__':
    if sys.argv[1] == 'dump':
        dump(sys.argv[2:])
