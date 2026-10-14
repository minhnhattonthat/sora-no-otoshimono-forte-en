"""Phase 3 gates: every string decodes and re-encodes to its original bytes; the rewrite walk matches extraction."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import extract  # noqa: E402
import insert  # noqa: E402
import romfs  # noqa: E402
import textfmt  # noqa: E402

ROM, IDS = romfs.load()
NAMES = [n for _, n in extract.chara_names(bytes(ROM.files[IDS['_Data/AdvTalk/CharaName.dat']]))]
SCRIPTS = [(p, bytes(ROM.files[f])) for p, f in sorted(IDS.items()) if extract.key_of(p)]


def test_counts():
    assert len(SCRIPTS) == 181
    assert sum(len(list(extract.strings(p, d, NAMES))) for p, d in SCRIPTS) == 20046


def test_decode_roundtrip():
    for p, d in SCRIPTS:
        for _, _, b in extract.strings(p, d, NAMES):
            assert textfmt.encode_ja(textfmt.decode(b)) == b, (p, b)


def test_rewrite_identity_and_order():
    for p, d in SCRIPTS:
        seen = []
        out = insert.rewrite(p, d, lambda i, k, old: seen.append((k, old)) or old)
        assert out == d, p
        assert seen == [(k, b) for k, _, b in extract.strings(p, d, NAMES)], p


def test_everything_translated():
    import json
    import arm9text
    import misctext
    missing = []
    for p, _ in SCRIPTS:
        key = extract.key_of(p)
        n = len(json.load(open(os.path.join(insert.ROOT, 'text', 'ja', key + '.json'), encoding='utf-8'))['lines'])
        en = insert.load_en(key)
        missing += [f'{key}#{i}' for i in range(n) if i not in en]
    assert not missing, missing[:10]
    tr = misctext.translator(misctext.load_en())
    ja = json.load(open(os.path.join(insert.ROOT, 'text', 'ja', 'misc.json'), encoding='utf-8'))
    assert not [s for v in ja.values() for s in v if tr(s.encode('cp932')) is None]
    a9 = open(os.path.join(insert.ROOT, 'work', 'arm9.bin'), 'rb').read() if os.path.exists(
        os.path.join(insert.ROOT, 'work', 'arm9.bin')) else None
    if a9:
        en = arm9text.load_en()
        assert not [t for _, _, t in arm9text.slots(a9) if t not in en]


def test_names_fit_plate():
    import batches
    adv = batches.adv_table()
    names = insert.load_names()
    assert len(names) == len(NAMES)
    for i, n in names.items():
        assert n.isascii() and sum(adv[ord(c)] for c in n) <= 72, (i, n)


def test_encode_en_even_units():
    b = textfmt.encode_en('Hi!\nYes{1F}{12}…')
    assert len(b) % 2 == 0
    for i in range(0, len(b), 2):
        if b[i] == 0x1b or b[i] >= 0x80:
            assert i % 2 == 0
    assert textfmt.encode_en('abc') == b'abc '
    assert textfmt.encode_en('ab\ncd') == b'ab\x1b\x01cd'
    assert textfmt.encode_en('a…') == b'a \x81\x63'
    assert textfmt.encode_en('TOMO☆KI♥') == b'TOMO^KI|'
