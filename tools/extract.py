"""Extract every script string to text/ja/<group>/<name>.json.

Each file: {"file": NitroFS path, "lines": [{"id", "kind", "spk", "ja"}]}. id = running index of the string in the
file (stable: the codec is byte-exact). kind: msg | name (custom speaker label) | choice.
Translations live in text/en/<group>/<name>.json as {id: English}.
python -X utf8 tools/extract.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import romfs  # noqa: E402
import script  # noqa: E402
import textfmt  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def key_of(path):
    """NitroFS path -> 'story/ch00_000' | 'chara/ch00_10_01_000' | 'trial/pack00', or None."""
    p = path.split('/')
    if path.startswith('_Data/Script/Other/Story/'):
        return f'story/ch{p[4][-2:]}_{p[5][:-4]}'
    if path.startswith('_Data/Script/Chara/'):
        return f'chara/ch{p[3][-2:]}_{p[4]}_{p[5][:-4]}'
    if path.startswith('_Data/Script/Trial/PackScript'):
        return f'trial/pack{p[3][10:12]}'
    return None


def chara_names(data):
    """_Data/AdvTalk/CharaName.dat: u8 count, then (u8 len, name, u32, u32, u8 k, k bytes) records."""
    n, pos, out = data[0], 1, []
    for _ in range(n):
        ln = data[pos]
        out.append((pos, data[pos + 1:pos + 1 + ln]))
        pos += 1 + ln + 8
        pos += 1 + data[pos]
    assert pos == len(data), (pos, len(data))
    return out


def commands(path, data):
    if path.startswith('_Data/Script/Trial/'):
        blocks, _ = script.parse_pack(data)
        return [c for _, cmds in blocks for c in cmds]
    return script.parse(data)[2]


def strings(path, data, names):
    """Yield (kind, speaker, bytes) in file order, matching insert.py's walk."""
    for c in commands(path, data):
        tup = [p for p in c.parts if isinstance(p, tuple)]
        if c.op in (0x03, 0xa9):
            sp = c.parts[0][0]
            spk = textfmt.decode(names[sp - 1]) if 0 < sp <= len(names) else ''
            if len(tup) == 2:
                yield 'name', spk, tup[0][1]
                spk = textfmt.decode(tup[0][1])
            yield 'msg', spk, tup[-1][1]
        else:
            for t in tup:
                yield 'choice', '', t[1]


def main():
    rom, ids = romfs.load()
    names = [n for _, n in chara_names(bytes(rom.files[ids['_Data/AdvTalk/CharaName.dat']]))]
    total = 0
    for path, fid in sorted(ids.items()):
        key = key_of(path)
        if not key:
            continue
        lines = [{'id': i, 'kind': k, 'spk': s, 'ja': textfmt.decode(b)}
                 for i, (k, s, b) in enumerate(strings(path, bytes(rom.files[fid]), names))]
        out = os.path.join(ROOT, 'text', 'ja', key + '.json')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8', newline='\n') as f:  # one entry per line: easy to read and diff
            f.write('{"file": %s, "lines": [\n' % json.dumps(path))
            f.write(',\n'.join(json.dumps(x, ensure_ascii=False) for x in lines))
            f.write('\n]}\n')
        total += len(lines)
    print('strings', total)


if __name__ == '__main__':
    main()
