"""String <-> text conversion for script strings, and the width model.

Text form: '\\n' = 1B 01, '{XX}' = 1B XX (hex), everything else is Shift-JIS (cp932) / ASCII.
Encoding English: the renderer walks 2-byte units, so before every control code or double-byte char, and at the
end, an odd length is padded with one space.
"""
import re

TOKEN = re.compile(r'\{([0-9A-F]{2})\}|\n')
# ☆ ♪ ♥ are drawn from unused ASCII slots (vwf.SYMBOLS) so they stay single-byte: no padding space before them
SYMBOLS = {'☆': b'^', '♪': b'`', '♥': b'|'}
LINE_PX = 216         # 18 full-width cells x 12 px; verified in-game (docs/re/script.md)
MAX_LINES = 3


def decode(b):
    out, i = [], 0
    while i < len(b):
        c = b[i]
        if c == 0x1b:
            out.append('\n' if b[i + 1] == 1 else '{%02X}' % b[i + 1])
            i += 2
        elif c >= 0x80:
            out.append(b[i:i + 2].decode('cp932'))
            i += 2
        else:
            out.append(chr(c))
            i += 1
    return ''.join(out)


def encode_ja(s):
    """Exact inverse of decode for original strings (no padding)."""
    out = bytearray()
    pos = 0
    for m in TOKEN.finditer(s):
        out += s[pos:m.start()].encode('cp932')
        out += b'\x1b\x01' if m.group() == '\n' else bytes([0x1b, int(m.group(1), 16)])
        pos = m.end()
    return bytes(out + s[pos:].encode('cp932'))


def encode_en(s):
    out = bytearray()

    def pad():
        if len(out) % 2:
            out.append(0x20)

    pos = 0
    pieces = []
    for m in TOKEN.finditer(s):
        pieces.append(('t', s[pos:m.start()]))
        pieces.append(('c', b'\x1b\x01' if m.group() == '\n' else bytes([0x1b, int(m.group(1), 16)])))
        pos = m.end()
    pieces.append(('t', s[pos:]))
    for kind, v in pieces:
        if kind == 'c':
            pad()
            out += v
            continue
        for ch in v:
            b = SYMBOLS[ch] if ch in SYMBOLS else ch.encode('cp932')
            if len(b) == 2:
                pad()
            out += b
    pad()
    return bytes(out)


def wrap(text, adv, px=LINE_PX):
    """Greedy word wrap of English to px per line; explicit '\\n' kept. Returns the text with '\\n' breaks."""
    out = []
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            cand = word if not line else line + ' ' + word
            if line and width(cand, adv) > px:
                out.append(line)
                line = word
            else:
                line = cand
        out.append(line)
    return '\n'.join(out)


def width(line, adv):
    """Pixel width of one line (no newlines) as the patched renderer lays it out: 2-byte units, double-byte = 12 px,
    ASCII pair = adv + adv (padding spaces included)."""
    b = encode_en(line)
    w = 0
    for i in range(0, len(b), 2):
        if b[i] == 0x1b:
            continue
        w += 12 if b[i] >= 0x80 else adv[b[i]] + adv[b[i + 1]]
    return w
