"""*_PACK.bin archives (EventList, Gallery, BackUp): u32 n, u32 size[n], u32 offset[n] (absolute), then the files.

python -X utf8 tools/pack.py list _Data/EventList/EVENTLIST_PACK.bin   -> index, size, magic of each entry
Entries are addressed elsewhere as "<pack path>#<index>" (gfxedit specs).
"""
import struct
import sys


def unpack(d):
    n = struct.unpack_from('<I', d, 0)[0]
    sizes = struct.unpack_from('<%dI' % n, d, 4)
    offs = struct.unpack_from('<%dI' % n, d, 4 + 4 * n)
    return [d[o:o + s] for o, s in zip(offs, sizes)]


def pack(entries, align=4):
    n = len(entries)
    pos = 4 + 8 * n
    offs, body = [], b''
    for e in entries:
        pad = -pos % align
        body += b'\0' * pad
        pos += pad
        offs.append(pos)
        body += e
        pos += len(e)
    return struct.pack('<%dI' % (1 + 2 * n), n, *map(len, entries), *offs) + body


def selftest(d):
    ents = unpack(d)
    assert unpack(pack(ents)) == ents


def groups(ents):
    """Image groups: (char index, palette index, screen index|None, cells index|None, dat index|None)."""
    out = []
    for i, e in enumerate(ents):
        if e[:4] != b'RGCN':
            continue
        g = {'char': i}
        for j in range(i + 1, min(i + 4, len(ents))):
            m = ents[j][:4]
            if m == b'RGCN':
                break
            key = {b'RLCN': 'palette', b'RCSN': 'screen', b'RECN': 'cells'}.get(m, 'dat')
            g.setdefault(key, j)
        out.append(g)
    return out


def specs_for(path, d):
    """Minimal gfxedit specs (no ops) for every image group in the pack."""
    out = []
    for g in groups(unpack(d)):
        s = {'file': f'{path}#{g["char"]}', 'ops': []}
        if 'palette' in g:
            s['palette'] = f'{path}#{g["palette"]}'
        if 'screen' in g:
            s['screen'] = f'{path}#{g["screen"]}'
        if 'cells' in g:
            s['cells'] = f'{path}#{g["cells"]}'
        out.append((g, s))
    return out


if __name__ == '__main__':
    sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
    import romfs
    rom, ids = romfs.load()
    d = bytes(rom.files[ids[sys.argv[2]]])
    selftest(d)
    if sys.argv[1] == 'list':
        for i, e in enumerate(unpack(d)):
            print(i, len(e), e[:4])
    elif sys.argv[1] == 'dump':  # PNG per image group -> work/gfx/<PACKNAME>/<char index>.png
        import os
        import gfxedit
        files = gfxedit.rom_files()
        name = sys.argv[2].rsplit('/', 1)[1].split('.')[0]
        out = os.path.join('work', 'gfx', name)
        os.makedirs(out, exist_ok=True)
        for g, s in specs_for(sys.argv[2], d):
            try:
                gfxedit.Canvas(s, files).rgb().save(os.path.join(out, '%03d.png' % g['char']))
            except Exception as e:
                print('skip', g, e)
        print(out)
