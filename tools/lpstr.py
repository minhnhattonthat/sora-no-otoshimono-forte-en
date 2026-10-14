"""Length-prefixed Shift-JIS strings in the small data files (u8 length + text, no terminator).

scan(data) finds every span where a byte L is followed by exactly L bytes of valid text containing Japanese,
and the next byte would start something else. Files whose structure has no offsets/sizes can then be rebuilt by
splicing (replace()). Files with size tables are handled in misctext.py on top of this.
"""
import re

JP = re.compile('[぀-ヿ一-鿿！-～…　-〿]')


def text_ok(b):
    i = 0
    while i < len(b):
        c = b[i]
        if 0x20 <= c < 0x7f:
            i += 1
        elif (0x81 <= c <= 0x9f or 0xe0 <= c <= 0xfc) and i + 1 < len(b) and 0x40 <= b[i + 1] <= 0xfc \
                and b[i + 1] != 0x7f:
            i += 2
        else:
            return False
    try:
        return bool(JP.search(b.decode('cp932')))
    except UnicodeDecodeError:
        return False


def scan(data, start=0):
    """-> list of (pos of length byte, bytes). Non-overlapping, greedy left to right."""
    out, i = [], start
    while i < len(data):
        n = data[i]
        if 2 <= n and i + 1 + n <= len(data) and text_ok(data[i + 1:i + 1 + n]):
            out.append((i, data[i + 1:i + 1 + n]))
            i += 1 + n
        else:
            i += 1
    return out


def replace(data, spans, new):
    """spans from scan(); new: {index: bytes}. Returns (bytes, delta per span start) for offset fix-ups."""
    out, last, shift = bytearray(), 0, []
    d = 0
    for k, (pos, old) in enumerate(spans):
        out += data[last:pos]
        shift.append((pos, d))
        b = new.get(k, old)
        if len(b) > 255:
            raise ValueError('string over 255 bytes')
        out += bytes([len(b)]) + b
        d += len(b) - len(old)
        last = pos + 1 + len(old)
    out += data[last:]
    return bytes(out), shift
