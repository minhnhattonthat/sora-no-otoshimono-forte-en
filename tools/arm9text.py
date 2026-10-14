"""Japanese strings in arm9 (system/error messages, delusion-mode prompts), patched in place.

python -X utf8 tools/arm9text.py  -> lists every slot: address, capacity, Japanese
Translations: text/en/arm9.json {"Japanese": "English"} ('\\n' allowed). A slot is the zero-terminated string plus
the zero padding up to the next 4-byte boundary; the English (+ terminator) must fit in it.
patch(main_section_bytes) is called from vwf.patch_arm9's caller (insert.py) before the arm9 is recompressed.
"""
import json
import os
import re
import sys

BASE = 0x2000000
ROOT = os.path.join(os.path.dirname(__file__), '..')
KANA = re.compile('[぀-ヿ]')


def slots(data):
    """-> [(offset, capacity, text)] for zero-terminated cp932 strings containing kana."""
    out = []
    for m in re.finditer(rb'(?:[\x81-\x9f\xe0-\xef][\x40-\x7e\x80-\xfc]|[\x20-\x7e\n]){3,}\x00', data):
        s = m.group()[:-1]
        try:
            t = s.decode('cp932')
        except UnicodeDecodeError:
            continue
        if len(KANA.findall(t)) < 3 or m.start() % 4:
            continue
        end = m.end()
        while end % 4:
            end += 1
        out.append((m.start(), end - m.start(), t))
    if data[0xC91A4:0xC91A9] == 'はい'.encode('cp932') + b'\0':  # 2-kana yes, too short for the scan
        out.append((0xC91A4, 8, 'はい'))
    return out


def load_en():
    p = os.path.join(ROOT, 'text', 'en', 'arm9.json')
    with open(p, encoding='utf-8') as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith('_')}


def patch(data):
    d = bytearray(data)
    en = load_en()
    for off, cap, t in slots(bytes(data)):
        if t not in en:
            continue
        b = en[t].encode('ascii')
        if len(b) + 1 > cap:
            raise ValueError(f'arm9 string too long ({len(b) + 1} > {cap}): {en[t]!r}')
        d[off:off + cap] = b + b'\0' * (cap - len(b))
    return bytes(d)


if __name__ == '__main__':
    d = open(os.path.join(ROOT, 'work', 'arm9.bin'), 'rb').read()
    for off, cap, t in slots(d):
        print(f'{BASE + off:08X} {cap:3d} {t!r}')
