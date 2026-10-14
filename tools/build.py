"""Build the ROM: insert text/ into the original image in place (tools/nds.py).

python -X utf8 tools/build.py [--identity] [--out build/sora-en.nds]
--identity: no edits; the output must equal the original (tests/test_identity.py).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import nds  # noqa: E402
import romfs  # noqa: E402


def build(out, identity=False):
    _, ids = romfs.load()
    rom = nds.Rom(romfs.ROM)
    if not identity:
        import insert
        insert.apply(rom, ids)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    rom.save(out)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--identity', action='store_true')
    ap.add_argument('--out', default='build/sora-en.nds')
    a = ap.parse_args()
    print(build(a.out, a.identity))
