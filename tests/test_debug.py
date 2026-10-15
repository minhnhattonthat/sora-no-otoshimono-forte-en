"""tools/debug/dbg.py: blank save layout and target -> jump.lua variables (no emulator needed)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'debug'))
import dbg  # noqa: E402


def test_blank_sav(tmp_path):
    p = tmp_path / 'b.dsv'
    dbg.blank_sav(str(p))
    d = p.read_bytes()
    assert len(d) == 65658 and d[:0x10000] == b'\xff' * 0x10000  # DeSmuME's 64 KB + 122-byte footer
    assert d.endswith(b'|-DESMUME SAVE-|')


def test_plan():
    assert dbg.plan('ep4')[0] == {'STORY': "'3,0'"}
    assert dbg.plan('ending7')[0] == {'STORY': "'6,7'"}
    assert dbg.plan('album')[0]['PROC'] == '13'
    assert dbg.plan('scene:20')[0]['PROC'] == '20'
    ev = dbg.plan('events4')[0]['EVENTS'].strip("'").split()
    assert len(ev) == 18 and ev[0] == '3,10,1'
