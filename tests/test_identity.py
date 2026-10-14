"""Phase 2 gates: unedited rebuild is byte-identical; every script round-trips through the codec."""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import nds  # noqa: E402
import romfs  # noqa: E402
import script  # noqa: E402

ORIG = open(romfs.ROM, 'rb').read()


def test_header_crc():
    assert struct.unpack_from('<H', ORIG, 0x15E)[0] == nds.crc16(ORIG[:0x15E])


def test_identity_build(tmp_path):
    import build
    out = build.build(str(tmp_path / 'id.nds'), identity=True)
    assert open(out, 'rb').read() == ORIG


def test_replace_same_and_grow():
    _, ids = romfs.load()
    rom = nds.Rom(romfs.ROM)
    fid = ids['_Data/AdvTalk/CharaName.dat']
    old = rom.read(fid)
    rom.replace(fid, old)
    assert rom.data == ORIG
    rom.replace(fid, old + b'x' * 4096)
    assert rom.read(fid) == old + b'x' * 4096
    assert struct.unpack_from('<H', rom.data, 0x15E)[0] == nds.crc16(rom.data[:0x15E])


def test_scripts_roundtrip():
    rom, ids = romfs.load()
    n = 0
    for p, fid in ids.items():
        if p.startswith(('_Data/Script/Other/', '_Data/Script/Chara/')):
            d = bytes(rom.files[fid])
            sid, unk, cmds, tail = script.parse(d)
            assert tail == b'', p
            assert script.build(sid, unk, cmds) == d, p
            n += 1
    assert n == 137


def test_trial_packs_block_length():
    """The first u16 of a pack block is its byte length - 4; the game stalls in Trial scenes if it is stale."""
    rom, ids = romfs.load()
    n = 0
    for p, fid in ids.items():
        if p.startswith('_Data/Script/Trial/'):
            d = bytes(rom.files[fid])
            blocks, tail = script.parse_pack(d)
            assert script.build_pack(blocks, tail) == d, p
            out = script.build_pack([(h, cmds[:-1]) for h, cmds in blocks], tail)  # shrink every block
            pos = 2
            for h, cmds in blocks:
                size = 11 + sum(len(c.encode()) for c in cmds[:-1])
                assert struct.unpack_from('<H', out, pos)[0] == size - 4, p
                pos += size
            n += 1
    assert n == 44
