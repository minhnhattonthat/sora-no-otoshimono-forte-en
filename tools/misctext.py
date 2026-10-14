"""Small data files with u8-length-prefixed strings: event titles, emblems, gallery lists, option help.

python -X utf8 tools/misctext.py   -> text/ja/misc.json (unique strings per file)
Translations: text/en/misc.json {"Japanese": "English"}. A Japanese string not found verbatim is matched by its
longest translated prefix + the untranslated rest (gallery labels like コミュニケーション0123 -> Communication 0123).
apply(rom, ids) is called by insert.py.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import lpstr  # noqa: E402
import romfs  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
SPLICE = ['_Data/EventList/EventData/0%d.dat' % i for i in range(6)] + [
    '_Data/EmblemList/emblem.dat', '_Data/Book/book01_chara.bin', '_Data/Book/book04_bgm.bin',
    '_Data/Book/book05_bg.bin']
SECTIONS = ['_Data/Book/book02_face.bin', '_Data/Book/book03_voice.bin']  # u32 n, u32 size[n], sections
TELOP = '_Data/Telop/telop_pack.bin'  # u32 n, u32 size[n], u32 offset[n] (4-aligned), sections
FILES = SPLICE + SECTIONS + [TELOP]


def splice(data, tr):
    spans = lpstr.scan(data)
    new = {k: tr(b) for k, (_, b) in enumerate(spans)}
    return lpstr.replace(data, spans, {k: v for k, v in new.items() if v is not None})


def rebuild(path, data, tr):
    if path in SPLICE:
        return splice(data, tr)[0]
    n = struct.unpack_from('<I', data, 0)[0]
    sizes = struct.unpack_from('<%dI' % n, data, 4)
    if path in SECTIONS:
        pos, out = 4 + 4 * n, []
        for s in sizes:
            out.append(splice(data[pos:pos + s], tr)[0])
            pos += s
        assert pos == len(data)
        return struct.pack('<%dI' % (n + 1), n, *map(len, out)) + b''.join(out)
    offs = struct.unpack_from('<%dI' % n, data, 4 + 4 * n)
    secs = [splice(data[o:o + s], tr)[0] for o, s in zip(offs, sizes)]
    body, new_offs = b'', []
    base = 4 + 8 * n
    for s in secs:
        new_offs.append(base + len(body))
        body += s + b'\0' * (-len(s) % 4)
    body = body[:len(body) - (-len(secs[-1]) % 4)] if data[-1:] != b'\0' else body  # original has no tail pad
    return struct.pack('<%dI' % (1 + 2 * n), n, *map(len, secs), *new_offs) + body


def load_en():
    p = os.path.join(ROOT, 'text', 'en', 'misc.json')
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith('_')}


def translator(en):
    keys = sorted(en, key=len, reverse=True)

    def enc(t):
        return t.replace('♥', 'Ω').encode('cp932')  # the font draws a heart at Ω

    def tr(b):
        s = b.decode('cp932')
        if s in en:
            return enc(en[s])
        for k in keys:
            if s.startswith(k) and s[len(k):].isascii():
                return enc(en[k] + s[len(k):])
        return None
    return tr


# Event titles longer than this crash the event-select screen (24 tested fine, 31 crashed; JP max is 22).
EVENT_MAX = 24


def apply(rom, ids):
    tr = translator(load_en())

    def tr_event(b):
        new = tr(b)
        if new is not None and len(new) > EVENT_MAX:
            raise ValueError(f'event title over {EVENT_MAX} bytes: {new!r}')
        return new

    for p in FILES:
        rom.replace(ids[p], rebuild(p, rom.read(ids[p]), tr_event if 'EventData' in p else tr))


def extract():
    rom, ids = romfs.load()
    out = {}
    for p in FILES:
        seen = []
        rebuild(p, bytes(rom.files[ids[p]]), lambda b: seen.append(b.decode('cp932')))
        out[p] = list(dict.fromkeys(seen))
    with open(os.path.join(ROOT, 'text', 'ja', 'misc.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print({p: len(v) for p, v in out.items()})


if __name__ == '__main__':
    extract()
