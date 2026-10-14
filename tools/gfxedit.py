"""Spec-driven edits of text drawn as graphics. One JSON spec per image under gfx/edits/ (see gfx/README.md).

python -X utf8 tools/gfxedit.py preview gfx/edits/ShowTitle/Chapter00.json [..]   -> work/gfx/preview/<spec>.png
python -X utf8 tools/gfxedit.py orig    gfx/edits/ShowTitle/Chapter00.json          -> work/gfx/preview/<spec>.orig.png
apply(rom, ids) (called by insert.py) writes every spec's result into the ROM.

Supported images: NCBR/NCGR bitmaps (linear), and tiled NCGR + NSCR backgrounds ("screen" in the spec).
Colors are "#rrggbb" (nearest palette entry, within the cell's 16-colour bank for 4 bpp BGs) or "transparent" (index 0).
"""
import glob
import json
import os
import struct
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import gfx  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
EDITS = os.path.join(ROOT, 'gfx', 'edits')


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, spec, files):
        self.spec = spec
        self.orig = files[spec['file']]
        self.char = gfx.Char(self.orig)
        pal_path = spec.get('palette') or sibling(spec['file'], '.NCLR')
        self.pal, _ = gfx.palette(files[pal_path])
        self.screen = spec.get('screen')
        self.cells = spec.get('cells')
        c = self.char
        if self.cells:
            self._init_cells(files[self.cells], spec.get('cell', 0))
        elif self.screen:
            raw = files[self.screen]
            self.nscr = bytearray(raw)
            s = gfx.section(raw, b'NRCS')
            self.sw, self.sh, _, size = struct.unpack_from('<HHII', raw, s + 8)
            self.ent_at = s + 0x14
            self.ents = list(struct.unpack_from('<%dH' % (size // 2), raw, self.ent_at))
            self.w, self.h = self.sw, self.sh
            self.idx = [[0] * self.w for _ in range(self.h)]
            self.bank = [[0] * self.w for _ in range(self.h)]
            cols = self.w // 8
            for k, e in enumerate(self.ents):
                bx, by = k % cols * 8, k // cols * 8
                if by >= self.h:
                    break
                t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
                tile = c.tile(t) or [0] * 64
                for i, v in enumerate(tile):
                    x, y = i % 8, i // 8
                    x, y = (7 - x if hf else x), (7 - y if vf else y)
                    self.idx[by + y][bx + x] = v
                    self.bank[by + y][bx + x] = p if c.bpp == 4 else 0
        else:
            if not c.linear:
                raise ValueError('tiled image without a screen: not supported yet (OBJ/NCER)')
            self.w, self.h = c.w, c.h
            self.idx = [c.idx[y * c.w:(y + 1) * c.w] for y in range(c.h)]
            self.bank = None
        self.before = [row[:] for row in self.idx]

    SIZES = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),
             (1, 0): (16, 8), (1, 1): (32, 8), (1, 2): (32, 16), (1, 3): (64, 32),
             (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}

    def _init_cells(self, ncer, cell):
        """Compose OBJ cell `cell` of an NCER (1D mapping) into one canvas; remember where each pixel came from."""
        d = gfx.container(gfx.unlz(ncer))
        s = gfx.section(d, b'KBEC')
        n, attr, off, mapping = struct.unpack_from('<HHII', d, s + 8)
        esz = 16 if attr == 1 else 8
        cbase = s + 8 + off
        nobj, _, ooff = struct.unpack_from('<HHI', d, cbase + cell * esz)
        obase = cbase + n * esz + ooff
        shift = mapping & 3  # 1D boundary: 0 = 32 KB (index * 1 tile), 1 = 64 KB (x2), 2 = 128 KB (x4), 3 = 256 KB (x8)
        c = self.char
        objs = []
        for i in range(nobj):
            a0, a1, a2 = struct.unpack_from('<HHH', d, obase + 6 * i)
            y = a0 & 0xFF
            y = y - 256 if y >= 128 else y
            x = a1 & 0x1FF
            x = x - 512 if x >= 256 else x
            w, h = self.SIZES[(a0 >> 14, a1 >> 14)]
            tile = (a2 & 0x3FF) << shift
            if c.bpp == 8:
                tile //= 2
            objs.append((x, y, w, h, tile, a1 >> 12 & 1, a1 >> 13 & 1, a2 >> 12))
        x0 = min(o[0] for o in objs)
        y0 = min(o[1] for o in objs)
        self.w = max(o[0] + o[2] for o in objs) - x0
        self.h = max(o[1] + o[3] for o in objs) - y0
        self.idx = [[0] * self.w for _ in range(self.h)]
        self.bank = [[0] * self.w for _ in range(self.h)] if c.bpp == 4 else None
        self.src = {}  # (x, y) -> flat pixel index in char data
        for x, y, w, h, tile, hf, vf, p in objs:
            tpr = w // 8
            for py in range(h):
                for px in range(w):
                    sx, sy = (w - 1 - px if hf else px), (h - 1 - py if vf else py)
                    if c.linear:  # NCBR: each OBJ's pixels are a plain w x h bitmap
                        k = tile * 64 + sy * w + sx
                    else:
                        t = tile + sy // 8 * tpr + sx // 8
                        k = t * 64 + sy % 8 * 8 + sx % 8
                    cx, cy = x - x0 + px, y - y0 + py
                    if k < len(c.idx):
                        self.idx[cy][cx] = c.idx[k]
                        self.src[(cx, cy)] = k
                    if self.bank:
                        self.bank[cy][cx] = p

    def color(self, x, y, spec):
        if spec == 'transparent':
            return 0
        r, g, b = int(spec[1:3], 16), int(spec[3:5], 16), int(spec[5:7], 16)
        base = self.bank[y][x] * 16 if self.bank else 0
        n = 16 if (self.bank is not None and self.char.bpp == 4) else len(self.pal)
        best, bi = None, 1
        for i in range(1, n):
            pr, pg, pb = self.pal[base + i] if base + i < len(self.pal) else (0, 0, 0)
            d = (pr - r) ** 2 + (pg - g) ** 2 + (pb - b) ** 2
            if best is None or d < best:
                best, bi = d, i
        return bi

    def rgb(self):
        img = Image.new('RGB', (self.w, self.h))
        px = img.load()
        for y in range(self.h):
            for x in range(self.w):
                base = self.bank[y][x] * 16 if self.bank else 0
                i = base + self.idx[y][x]
                px[x, y] = self.pal[i] if i < len(self.pal) else (255, 0, 255)
        return img

    def encode(self):
        c = self.char
        if self.cells:
            flat = list(c.idx)
            for (x, y), k in self.src.items():
                flat[k] = self.idx[y][x]
            return c.encode(flat, self.orig), None
        if not self.screen:
            flat = [v for row in self.idx for v in row]
            return c.encode(flat + c.idx[len(flat):], self.orig), None
        tiles = list(c.idx)
        cols = self.w // 8
        refs = {}
        for e in self.ents:
            refs[e & 0x3FF] = refs.get(e & 0x3FF, 0) + 1
        for k, e in enumerate(self.ents):
            bx, by = k % cols * 8, k // cols * 8
            if by >= self.h:
                break
            block = [self.idx[by + i // 8][bx + i % 8] for i in range(64)]
            old = [self.before[by + i // 8][bx + i % 8] for i in range(64)]
            if block == old:
                continue
            t = e & 0x3FF
            if refs[t] == 1:
                tiles[t * 64:(t + 1) * 64] = block
            else:
                refs[t] -= 1
                t = len(tiles) // 64
                tiles += block
                refs[t] = 1
            self.ents[k] = (e & 0xF000) | t  # flips cleared: the block is stored as displayed
        nscr = self.nscr
        struct.pack_into('<%dH' % len(self.ents), nscr, self.ent_at, *self.ents)
        return c.encode(tiles, self.orig), bytes(nscr)


def sibling(path, ext):
    base = path.rsplit('.', 1)[0].replace('_LZ', '')
    return base + ext


# ---------------------------------------------------------------- fonts
class NitroFont:
    """Draw with the game's own NFTR glyphs; ASCII gets proportional spacing like the dialogue VWF."""

    def __init__(self, data, space=3):
        import vwf
        f = vwf.font_widths(data)[0]
        self.f = f
        plgc = struct.unpack_from('<I', f, 0x10 + 0x10)[0]
        self.hdwc = struct.unpack_from('<I', f, 0x10 + 0x14)[0]
        self.cw, self.ch, self.tsz = struct.unpack_from('<BBH', f, plgc)
        self.bpp = f[plgc + 6]
        self.glyphs = plgc + 8
        self.height = self.ch
        self.vwf = vwf

    def glyph(self, ch):
        code = ord(ch) if ord(ch) < 0x80 else int.from_bytes(ch.encode('cp932'), 'big')
        g = code - 0x20 if code < 0x80 else self.vwf.glyph_index(self.f, code)
        left, ink, adv = self.f[self.hdwc + 8 + 3 * g:self.hdwc + 11 + 3 * g]
        bits = ''.join(f'{b:08b}' for b in self.f[self.glyphs + g * self.tsz:self.glyphs + (g + 1) * self.tsz])
        pts = [(x + left, y) for y in range(self.ch) for x in range(self.cw)
               if bits[(y * self.cw + x) * self.bpp] == '1']
        return pts, adv

    def width(self, s):
        return sum(self.glyph(c)[1] for c in s)

    def mask(self, s):
        pts, x = [], 0
        for c in s:
            p, adv = self.glyph(c)
            pts += [(x + a, b) for a, b in p]
            x += adv
        return pts


class TTF:
    def __init__(self, path, size):
        self.font = ImageFont.truetype(path, size)
        a, d = self.font.getmetrics()
        self.height = a + d

    def width(self, s):
        return int(self.font.getlength(s))

    def mask(self, s):
        w = max(1, self.width(s) + 4)
        im = Image.new('1', (w, self.height + 2), 0)
        ImageDraw.Draw(im).text((0, 0), s, font=self.font, fill=1)
        px = im.load()
        return [(x, y) for y in range(im.height) for x in range(im.width) if px[x, y]]


def load_font(spec, files):
    if spec in ('f12', 'f10'):
        name = {'f12': '_Data/font/Font1212.NFTR', 'f10': '_Data/font/Font1010.NFTR'}[spec]
        return NitroFont(files[name])
    path, size = spec.rsplit(':', 1)  # "comicbd.ttf:14" (Windows font dir) or "C:/path/font.ttf:14"
    if not os.path.isabs(path):
        path = os.path.join('C:/Windows/Fonts', path)
    return TTF(path, int(size))


# ---------------------------------------------------------------- ops
def op_fill(cv, op):
    x0, y0, w, h = op['rect']
    for y in range(y0, min(y0 + h, cv.h)):
        for x in range(x0, min(x0 + w, cv.w)):
            cv.idx[y][x] = cv.color(x, y, op['color'])


def op_copy(cv, op):
    x0, y0, w, h = op['from']
    tx, ty = op['to']
    block = [[cv.idx[y][x] for x in range(x0, x0 + w)] for y in range(y0, y0 + h)]
    for dy, row in enumerate(block):
        for dx, v in enumerate(row):
            if 0 <= ty + dy < cv.h and 0 <= tx + dx < cv.w:
                cv.idx[ty + dy][tx + dx] = v


def op_erase(cv, op):
    """Replace pixels whose colour is in op['colors'] (inside rect) by the nearest other pixel on the same row."""
    x0, y0, w, h = op['rect']
    kill = set()
    for c in op['colors']:
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        kill.add((r, g, b))
    tol = op.get('tolerance', 24)

    def is_kill(x, y):
        base = cv.bank[y][x] * 16 if cv.bank else 0
        pr, pg, pb = cv.pal[base + cv.idx[y][x]]
        return any(abs(pr - r) + abs(pg - g) + abs(pb - b) <= tol for r, g, b in kill)

    for y in range(y0, min(y0 + h, cv.h)):
        row = list(range(x0, min(x0 + w, cv.w)))
        bad = [x for x in row if is_kill(x, y)]
        good = [x for x in row if x not in set(bad)]
        if not good:
            continue
        for x in bad:
            nx = min(good, key=lambda g: abs(g - x))
            cv.idx[y][x] = cv.idx[y][nx]


def wrap(font, text, width):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split(' '):
            cand = word if not cur else cur + ' ' + word
            if cur and font.width(cand) > width:
                lines.append(cur)
                cur = word
            else:
                cur = cand
        lines.append(cur)
    return lines


def op_text(cv, op, files):
    font = load_font(op.get('font', 'f12'), files)
    x0, y0, w, h = op['rect']
    lines = wrap(font, op['text'], w) if op.get('wrap', True) else op['text'].split('\n')
    lh = op.get('lineh', font.height + 1)
    total = lh * len(lines)
    va = op.get('valign', 'top')
    y = y0 + (0 if va == 'top' else (h - total) // 2 if va == 'middle' else h - total)
    ol = op.get('outline')
    sh = op.get('shadow')
    pts_all = []
    for ln in lines:
        lw = font.width(ln)
        al = op.get('align', 'left')
        x = x0 + (0 if al == 'left' else (w - lw) // 2 if al == 'center' else w - lw)
        pts_all += [(x + a, y + b) for a, b in font.mask(ln)]
        y += lh
    if op.get('bold'):
        pts_all += [(a + 1, b) for a, b in pts_all]
    ink = set(pts_all)

    def put(x, y, col):
        if 0 <= x < cv.w and 0 <= y < cv.h:
            cv.idx[y][x] = cv.color(x, y, col)

    if sh:
        for a, b in ink:
            if (a + 1, b + 1) not in ink:
                put(a + 1, b + 1, sh)
    if ol:
        ring = set()
        for a, b in ink:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if (a + dx, b + dy) not in ink:
                        ring.add((a + dx, b + dy))
        for a, b in ring:
            put(a, b, ol)
    for a, b in ink:
        put(a, b, op['color'])
    over = [p for p in ink if not (x0 <= p[0] < x0 + w and y0 <= p[1] < y0 + h)]
    if over and not op.get('allow_overflow'):
        raise ValueError(f'text overflows its rect: {op["text"]!r}')


def op_layout(cv, op, files):
    """Change rect `index` of a texture layout .dat (u8 count, then 5-byte x0,y0,x1,y1,flag entries; inclusive)."""
    path = op['dat']
    d = bytearray(cv.extra.get(path, files[path]))
    assert op['index'] < d[0]
    o = 1 + 5 * op['index']
    d[o:o + 4] = bytes(op['rect'])
    cv.extra[path] = bytes(d)


OPS = {'fill': op_fill, 'copy': op_copy, 'erase': op_erase}


def run(spec, files):
    cv = Canvas(spec, files)
    cv.extra = {}
    for op in spec['ops']:
        if op['op'] == 'text':
            op_text(cv, op, files)
        elif op['op'] == 'layout':
            op_layout(cv, op, files)
        else:
            OPS[op['op']](cv, op)
    return cv


# ---------------------------------------------------------------- entry points
def specs():
    for p in sorted(glob.glob(os.path.join(EDITS, '**', '*.json'), recursive=True)):
        with open(p, encoding='utf-8') as f:
            yield p, json.load(f)


def rom_files():
    import romfs
    rom, ids = romfs.load()

    class Files(dict):
        def __missing__(self, k):
            v = bytes(rom.files[ids[k]])
            self[k] = v
            return v
    return Files()


def apply(rom, ids):
    files = {}

    class Files(dict):
        def __missing__(self, k):
            v = rom.read(ids[k])
            self[k] = v
            return v
    for p, spec in specs():
        files = Files()  # fresh per spec: several specs may edit the same file (different cells) in turn
        cv = run(spec, files)
        char, nscr = cv.encode()
        rom.replace(ids[spec['file']], char)
        if nscr:
            rom.replace(ids[cv.screen], nscr)
        for path, data in cv.extra.items():
            rom.replace(ids[path], data)


def main():
    cmd, paths = sys.argv[1], sys.argv[2:]
    files = rom_files()
    out = os.path.join(ROOT, 'work', 'gfx', 'preview')
    os.makedirs(out, exist_ok=True)
    for p in paths:
        with open(p, encoding='utf-8') as f:
            spec = json.load(f)
        name = os.path.relpath(p, EDITS).replace(os.sep, '_')[:-5]
        if cmd == 'orig':
            cv = Canvas(spec, files)
            cv.rgb().save(os.path.join(out, name + '.orig.png'))
        else:
            cv = run(spec, files)
            cv.encode()  # proves it re-encodes
            img = cv.rgb()
            z = spec.get('preview_zoom', 2)
            img.resize((img.width * z, img.height * z), Image.NEAREST).save(os.path.join(out, name + '.png'))
        print(os.path.join(out, name + ('.orig' if cmd == 'orig' else '') + '.png'))


if __name__ == '__main__':
    main()
